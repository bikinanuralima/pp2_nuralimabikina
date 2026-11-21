"""Cuts Mickey's hands out of the photo and builds a hand-less background.
Run:  python3 build_assets.py <photo.jpeg>   (needs opencv-python, numpy, pillow)"""
import json, math, sys
import cv2, numpy as np
from PIL import Image

SRC = sys.argv[1] if len(sys.argv) > 1 else "images/mickeyclock.jpeg"
OUT = "images/"
PIVOT = (700, 523)               # hub of the clock in the photo
CROP = (280, 110, 1120, 950)     # square around the dial (x0, y0, x1, y1)
BAND = (46, 46, 50)              # sleeve colour sampled from the photo

img = cv2.cvtColor(cv2.imread(SRC), cv2.COLOR_BGR2RGB)
H, W = img.shape[:2]
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

def poly_mask(pts):
    m = np.zeros((H, W), np.uint8)
    cv2.fillPoly(m, [np.array(pts, np.int32)], 255)
    return m

def band_mask(angle_deg, length, width, start=0):
    """Rectangle from the pivot outwards; angle is clockwise from 12 o'clock."""
    a = math.radians(angle_deg)
    u = np.array([math.sin(a), -math.cos(a)]); n = np.array([-u[1], u[0]])
    p = np.array(PIVOT, float)
    pts = [p + u*start + n*width/2, p + u*length + n*width/2,
           p + u*length - n*width/2, p + u*start - n*width/2]
    return poly_mask(pts)

def glove_mask(pts):
    """Everything enclosed by the dark outline inside a generous polygon."""
    P = poly_mask(pts)
    dark = ((gray < 120) & (P > 0)).astype(np.uint8) * 255
    dark = cv2.dilate(dark, np.ones((3, 3), np.uint8))
    free = ((P > 0) & (dark == 0)).astype(np.uint8)
    # flood the outside from every free pixel on the polygon border
    border = cv2.dilate(P, np.ones((3, 3), np.uint8)) - cv2.erode(P, np.ones((3, 3), np.uint8))
    seeds = ((border > 0) & (free > 0)).astype(np.uint8)
    n, lab = cv2.connectedComponents(free, connectivity=4)
    outside_labels = set(np.unique(lab[seeds > 0])) - {0}
    outside = np.isin(lab, list(outside_labels))
    inside = (P > 0) & ~outside
    inside = cv2.morphologyEx(inside.astype(np.uint8)*255, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    return inside

# ---- right arm (viewer's right: the long pointing arm) ----
R_ANGLE, R_LEN = 60.5, 140
R_glove = glove_mask([(808,445),(812,418),(836,396),(876,378),(904,362),(929,362),(930,392),
                      (934,428),(925,449),(895,470),(860,476),(826,474),(808,464)])
# ---- left arm (viewer's left: shorter, hand at the cheek) ----
L_ANGLE, L_LEN = 305.0, 108
L_glove = glove_mask([(522,400),(545,386),(580,382),(606,380),(618,384),(640,380),(650,392),
                      (648,440),(642,468),(628,482),(600,486),(572,472),(545,445),(522,420)])


def largest(m):
    n, lab, stats, _ = cv2.connectedComponentsWithStats((m > 0).astype(np.uint8), connectivity=8)
    k = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
    return ((lab == k) * 255).astype(np.uint8)

R_glove, L_glove = largest(R_glove), largest(L_glove)

# sleeves are synthetic bars from the hub (same colour as the photo's sleeves)
R_band = band_mask(R_ANGLE, R_LEN, 19)
L_band = band_mask(L_ANGLE, L_LEN, 23)

def make_sprite(name, glove, band):
    # photo pixels for the glove, flat colour for the sleeve (glove drawn on top)
    rgb = img.copy()
    rgb[band > 0] = BAND
    alpha = np.maximum(glove, band)
    glove_on_top = glove > 0
    rgb[glove_on_top] = img[glove_on_top]
    # soften the edge a little, shave 1px to avoid a light fringe
    a = cv2.erode(alpha, np.ones((3, 3), np.uint8))
    a = cv2.GaussianBlur(a, (0, 0), 0.9)
    ys, xs = np.where(alpha > 0)
    pad = 6
    x0, x1, y0, y1 = xs.min()-pad, xs.max()+pad, ys.min()-pad, ys.max()+pad
    # keep the pivot inside the crop and make rotation about it simple
    x0, y0 = min(x0, PIVOT[0]-30), min(y0, PIVOT[1]-30)
    x1, y1 = max(x1, PIVOT[0]+30), max(y1, PIVOT[1]+30)
    out = np.dstack([rgb, a])[y0:y1, x0:x1]
    Image.fromarray(out, "RGBA").save(OUT + name)
    return [int(PIVOT[0]-x0), int(PIVOT[1]-y0)]

meta = {
    "right": {"file": "hand_right.png", "pivot": make_sprite("hand_right.png", R_glove, R_band), "rest_angle": R_ANGLE},
    "left":  {"file": "hand_left.png",  "pivot": make_sprite("hand_left.png",  L_glove, L_band), "rest_angle": L_ANGLE},
}

# hub knob (drawn on top of the hands)
hub_r = 22
hub = np.zeros((H, W), np.uint8); cv2.circle(hub, PIVOT, hub_r, 255, -1)
hub = cv2.GaussianBlur(hub, (0, 0), 0.9)
x0, y0 = PIVOT[0]-hub_r-2, PIVOT[1]-hub_r-2
Image.fromarray(np.dstack([img, hub])[y0:y0+2*hub_r+4, x0:x0+2*hub_r+4], "RGBA").save(OUT + "hub.png")
meta["hub"] = {"file": "hub.png", "pivot": [hub_r+2, hub_r+2]}

# background: photo with both hands removed
rm = np.maximum.reduce([R_glove, L_glove, R_band, L_band])
# the real left sleeve is wider than the bar, so also remove its dark patch next to the cuff
extra = poly_mask([(596,476),(626,466),(646,476),(650,512),(634,516),(618,500),(598,482)])
rm = np.maximum(rm, extra)
real_r_band = poly_mask([(700,522),(716,500),(742,484),(828,438),(842,466),(760,512),(716,534)])   # real right sleeve + shadow
rm = np.maximum(rm, real_r_band)
rm = cv2.dilate(rm, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (21, 21)))
bg = img.copy()
known = rm == 0
cx0, cy0 = PIVOT
HEAD_C, HEAD_R = (699, 421), 92      # head circle (hidden behind the left thumb)
ys, xs = np.where(rm > 0)
fill = bg.copy()
for y, x in zip(ys.tolist(), xs.tolist()):
    dxh, dyh = x - HEAD_C[0], y - HEAD_C[1]
    dh = math.hypot(dxh, dyh)
    if x < 665 and dh < HEAD_R - 3:        # inside the head: white face
        fill[y, x] = (252, 252, 252)
        continue
    if x < 665 and dh < HEAD_R + 1 and y < 470:   # head outline
        fill[y, x] = (34, 34, 38)
        continue
    dx, dy = x - cx0, y - cy0
    r = math.hypot(dx, dy)
    if r < 1:
        fill[y, x] = BAND
        continue
    ang0 = math.atan2(dy, dx)
    result = None
    for off in (0, 2, -2, 4, -4, 7, -7, 11, -11):      # try neighbouring rays if this one is blocked
        a_ = ang0 + math.radians(off)
        ux, uy = math.cos(a_), math.sin(a_)
        vals = []
        for sign in (-1, 1):
            for d in range(3, 330, 2):
                rr = r + sign*d
                px, py = int(round(cx0 + ux*rr)), int(round(cy0 + uy*rr))
                if 0 <= px < W and 0 <= py < H and known[py, px] and gray[py, px] > 212 and math.hypot(px-HEAD_C[0], py-HEAD_C[1]) > HEAD_R + 3:
                    vals.append((d, img[py, px].astype(float))); break
        if len(vals) == 2:
            (d0, c0), (d1, c1) = vals; t = d0/(d0+d1)
            result = c0*(1-t) + c1*t; break
        if vals and off == 0:
            result = vals[0][1]
    if result is not None:
        fill[y, x] = np.clip(result, 0, 255).astype(np.uint8)
bg = fill
bg = cv2.GaussianBlur(bg, (0, 0), 0.8) * 0 + np.where((cv2.dilate(rm, np.ones((5,5),np.uint8))>0)[...,None], cv2.GaussianBlur(bg,(0,0),0.8), bg)
# put a round "shoulder" under the hub so the arms look attached
sh = np.zeros((H, W), np.uint8); cv2.circle(sh, PIVOT, 34, 255, -1); sh = cv2.GaussianBlur(sh, (0,0), 1.2)
bg = (bg*(1-sh[...,None]/255.) + np.array(BAND)*(sh[...,None]/255.)).astype(np.uint8)
x0, y0, x1, y1 = CROP
Image.fromarray(bg[y0:y1, x0:x1]).save(OUT + "clock_face.png")
meta["center"] = [PIVOT[0]-x0, PIVOT[1]-y0]
meta["face_size"] = [x1-x0, y1-y0]
json.dump(meta, open(OUT + "hands.json", "w"), indent=2)
print(json.dumps(meta))
