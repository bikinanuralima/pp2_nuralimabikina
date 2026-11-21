"""Clock logic + drawing for Mickey's Clock.

The hands are cut out of the photo (images/hand_left.png, hand_right.png) and
rotated around Mickey's hub with pygame.transform.rotate().
"""
import json
import os
import time

import pygame

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, "images")

# On screen, the long pointing arm is on the right and the short one on the left.
# Right hand = minutes, left hand = seconds. Set True to swap them.
SWAP_HANDS = False


def get_time():
    """Return (minutes, seconds) from the system clock.

    tm_sec can be 60 or 61 during a leap second, so wrap it back into 0-59.
    """
    now = time.localtime()
    return now.tm_min, now.tm_sec % 60


def second_angle(seconds):
    """Clockwise degrees from 12 o'clock for the seconds hand."""
    return seconds * 6.0


def minute_angle(minutes, seconds):
    """Clockwise degrees for the minutes hand (creeps forward with seconds)."""
    return minutes * 6.0 + seconds * 0.1


def blit_rotate(surf, image, pos, pivot, angle):
    """Rotate `image` around `pivot` (a pixel inside the image) and draw it so
    that the pivot lands on `pos`. `angle` is pygame's counter-clockwise degrees.
    Technique from https://stackoverflow.com/a/54714144
    """
    image_rect = image.get_rect(topleft=(pos[0] - pivot[0], pos[1] - pivot[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
    rotated_offset = offset_center_to_pivot.rotate(-angle)
    rotated_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)
    rotated_image = pygame.transform.rotate(image, angle)
    surf.blit(rotated_image, rotated_image.get_rect(center=rotated_center))


class MickeyClock:
    def __init__(self, size):
        """`size` = width/height in pixels of the square clock window.
        Call after pygame.display.set_mode() (convert_alpha needs a display)."""
        with open(os.path.join(IMG_DIR, "hands.json")) as f:
            meta = json.load(f)

        self.size = size
        self.scale = size / float(meta["face_size"][0])
        self.center = (meta["center"][0] * self.scale, meta["center"][1] * self.scale)

        self.face, _ = self._load("clock_face.png")
        self.hub, self.hub_pivot = self._load(meta["hub"]["file"], meta["hub"]["pivot"])

        right, left = meta["right"], meta["left"]
        self.right_hand, self.right_pivot = self._load(right["file"], right["pivot"])
        self.left_hand, self.left_pivot = self._load(left["file"], left["pivot"])
        # the angle (clockwise from 12) each arm points at in the original photo
        self.right_rest = right["rest_angle"]
        self.left_rest = left["rest_angle"]

    def _load(self, filename, pivot=(0, 0)):
        img = pygame.image.load(os.path.join(IMG_DIR, filename)).convert_alpha()
        w, h = img.get_size()
        img = pygame.transform.smoothscale(img, (max(1, int(w * self.scale)), max(1, int(h * self.scale))))
        return img, (pivot[0] * self.scale, pivot[1] * self.scale)

    def _draw_hand(self, screen, image, pivot, rest_angle, target_angle):
        # pygame rotates counter-clockwise, a clock turns clockwise -> negate
        blit_rotate(screen, image, self.center, pivot, -(target_angle - rest_angle))

    def draw(self, screen):
        minutes, seconds = get_time()
        screen.blit(self.face, (0, 0))

        min_angle = minute_angle(minutes, seconds)
        sec_angle = second_angle(seconds)
        if SWAP_HANDS:
            self._draw_hand(screen, self.left_hand, self.left_pivot, self.left_rest, min_angle)
            self._draw_hand(screen, self.right_hand, self.right_pivot, self.right_rest, sec_angle)
        else:
            self._draw_hand(screen, self.left_hand, self.left_pivot, self.left_rest, sec_angle)
            self._draw_hand(screen, self.right_hand, self.right_pivot, self.right_rest, min_angle)

        screen.blit(self.hub, (self.center[0] - self.hub_pivot[0], self.center[1] - self.hub_pivot[1]))
        return minutes, seconds
