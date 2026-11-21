"""Drawing helpers for the Paint app (TSIS2): shapes, brush sizes, flood fill, text box.

Everything here uses only pygame's built-in drawing / Surface functions.
"""
import math

import pygame

# ----------------------------------------------------------------------------
# Tool names
# ----------------------------------------------------------------------------
PENCIL = "pencil"
LINE = "line"
RECT = "rect"
SQUARE = "square"
CIRCLE = "circle"
RIGHT_TRI = "right_tri"
EQUI_TRI = "equi_tri"
RHOMBUS = "rhombus"
ERASER = "eraser"
FILL = "fill"
TEXT = "text"
PICKER = "picker"

# tools that are drawn by dragging from a start point to an end point
SHAPE_TOOLS = (LINE, RECT, SQUARE, CIRCLE, RIGHT_TRI, EQUI_TRI, RHOMBUS)

# ----------------------------------------------------------------------------
# Brush sizes (keys 1 / 2 / 3 or the S / M / L buttons)
# ----------------------------------------------------------------------------
BRUSH_SIZES = {1: 2, 2: 5, 3: 10}         # small, medium, large (pixels)
ERASER_FACTOR = 3                         # eraser is 3x wider than the brush
TEXT_SIZES = {1: 20, 2: 32, 3: 48}        # font size follows the brush level


# ----------------------------------------------------------------------------
# Basic strokes
# ----------------------------------------------------------------------------
def draw_dot(surface, color, pos, width):
    """A single round dot (used when the mouse is clicked without moving)."""
    pygame.draw.circle(surface, color, (int(pos[0]), int(pos[1])), max(1, width // 2))


def draw_line(surface, color, start, end, width):
    """Thick line with round ends, so consecutive segments join smoothly."""
    a = (int(start[0]), int(start[1]))
    b = (int(end[0]), int(end[1]))
    pygame.draw.line(surface, color, a, b, width)
    if width > 1:
        r = max(1, width // 2)
        pygame.draw.circle(surface, color, a, r)
        pygame.draw.circle(surface, color, b, r)


def draw_polygon_outline(surface, color, points, width):
    """Closed outline with the given thickness (round joints at every corner)."""
    pts = [(int(x), int(y)) for x, y in points]
    pygame.draw.lines(surface, color, True, pts, width)
    if width > 1:
        r = max(1, width // 2)
        for p in pts:
            pygame.draw.circle(surface, color, p, r)


# ----------------------------------------------------------------------------
# Shape geometry (start = where the mouse went down, end = current position)
# ----------------------------------------------------------------------------
def shape_points(tool, start, end):
    """Corner points of a polygon tool. Returns [] if the shape would be empty."""
    x0, y0 = start
    x1, y1 = end
    dx, dy = x1 - x0, y1 - y0

    if tool == RECT:
        if dx == 0 or dy == 0:
            return []
        return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]

    if tool == SQUARE:
        side = max(abs(dx), abs(dy))
        if side == 0:
            return []
        sx = 1 if dx >= 0 else -1
        sy = 1 if dy >= 0 else -1
        xe, ye = x0 + sx * side, y0 + sy * side
        return [(x0, y0), (xe, y0), (xe, ye), (x0, ye)]

    if tool == RIGHT_TRI:
        # right angle in the corner below the start point
        if dx == 0 or dy == 0:
            return []
        return [(x0, y0), (x0, y1), (x1, y1)]

    if tool == EQUI_TRI:
        side = abs(dx)
        if side == 0:
            return []
        h = side * math.sqrt(3) / 2.0
        s = 1 if dy >= 0 else -1                 # drag down -> base below the apex
        return [((x0 + x1) / 2.0, y0), (x1, y0 + s * h), (x0, y0 + s * h)]

    if tool == RHOMBUS:
        if dx == 0 or dy == 0:
            return []
        cx, cy = (x0 + x1) / 2.0, (y0 + y1) / 2.0
        return [(cx, min(y0, y1)), (max(x0, x1), cy), (cx, max(y0, y1)), (min(x0, x1), cy)]

    return []


def draw_shape(surface, tool, color, start, end, width):
    """Draw LINE / RECT / SQUARE / CIRCLE / RIGHT_TRI / EQUI_TRI / RHOMBUS.
    `width` is the active brush size and applies to every shape."""
    if tool == LINE:
        draw_line(surface, color, start, end, width)
    elif tool == CIRCLE:
        radius = int(math.hypot(end[0] - start[0], end[1] - start[1]))
        if radius >= 1:
            center = (int(start[0]), int(start[1]))
            pygame.draw.circle(surface, color, center, radius, min(width, radius))
    else:
        pts = shape_points(tool, start, end)
        if pts:
            draw_polygon_outline(surface, color, pts, width)


# ----------------------------------------------------------------------------
# Flood fill (scan-line, uses Surface.get_at / Surface.set_at only)
# ----------------------------------------------------------------------------
def _rgb(surface, x, y):
    return tuple(surface.get_at((x, y)))[:3]


def flood_fill(surface, pos, new_color):
    """Fill the region containing `pos` with `new_color`.

    The fill spreads over pixels whose colour is exactly the colour that was
    clicked and stops at any pixel of a different colour.
    """
    w, h = surface.get_size()
    x, y = int(pos[0]), int(pos[1])
    if not (0 <= x < w and 0 <= y < h):
        return
    new = tuple(new_color)[:3]
    target = _rgb(surface, x, y)
    if target == new:
        return                                   # nothing to do (and avoids looping forever)

    stack = [(x, y)]
    while stack:
        x, y = stack.pop()
        if _rgb(surface, x, y) != target:        # already filled via another span
            continue
        left = x
        while left > 0 and _rgb(surface, left - 1, y) == target:
            left -= 1
        right = x
        while right < w - 1 and _rgb(surface, right + 1, y) == target:
            right += 1
        for xi in range(left, right + 1):
            surface.set_at((xi, y), new)
        # queue one seed per run of target-coloured pixels in the rows above and below
        for ny in (y - 1, y + 1):
            if 0 <= ny < h:
                in_run = False
                for xi in range(left, right + 1):
                    if _rgb(surface, xi, ny) == target:
                        if not in_run:
                            stack.append((xi, ny))
                            in_run = True
                    else:
                        in_run = False


# ----------------------------------------------------------------------------
# Text tool state
# ----------------------------------------------------------------------------
class TextBox:
    """Text being typed. `pos` is the top-left corner on the canvas."""

    def __init__(self, pos):
        self.pos = (int(pos[0]), int(pos[1]))
        self.content = ""
