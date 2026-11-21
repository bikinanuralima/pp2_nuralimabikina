"""Paint (TSIS2) - pencil, line, shapes, eraser, flood fill, text, brush sizes, save.

Run:  python3 paint.py
"""
import datetime
import os

import pygame

import tools

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_DIR = os.path.join(BASE_DIR, "saves")

WIDTH, HEIGHT = 1100, 720
TOOLBAR_H = 112
CANVAS_RECT = pygame.Rect(0, TOOLBAR_H, WIDTH, HEIGHT - TOOLBAR_H)
CANVAS_BG = (255, 255, 255)
PANEL = (222, 226, 234)
BTN = (245, 246, 250)
BTN_ACTIVE = (120, 170, 245)
BORDER = (90, 90, 100)
TEXT_COLOR = (30, 30, 40)

# (tool, label, shortcut key)
TOOL_BUTTONS = [
    (tools.PENCIL, "Pencil", "p"),
    (tools.LINE, "Line", "l"),
    (tools.RECT, "Rect", "r"),
    (tools.SQUARE, "Square", "s"),
    (tools.CIRCLE, "Circle", "c"),
    (tools.RIGHT_TRI, "R-Tri", "g"),
    (tools.EQUI_TRI, "Eq-Tri", "e"),
    (tools.RHOMBUS, "Rhombus", "d"),
    (tools.ERASER, "Eraser", "x"),
    (tools.FILL, "Fill", "f"),
    (tools.TEXT, "Text", "t"),
    (tools.PICKER, "Picker", "i"),
]

PALETTE = [
    (0, 0, 0), (255, 255, 255), (128, 128, 128), (200, 30, 30),
    (255, 140, 0), (250, 220, 0), (40, 170, 60), (0, 110, 50),
    (0, 200, 220), (40, 90, 230), (20, 30, 120), (140, 60, 190),
    (240, 120, 180), (120, 70, 30), (245, 222, 179), (170, 215, 255),
]

SIZE_LABELS = {1: "S  2px", 2: "M  5px", 3: "L  10px"}
SIZE_KEYS = {pygame.K_1: 1, pygame.K_2: 2, pygame.K_3: 3,
             pygame.K_KP1: 1, pygame.K_KP2: 2, pygame.K_KP3: 3}


class PaintApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Paint - TSIS2")
        self.clock = pygame.time.Clock()

        self.canvas = pygame.Surface((CANVAS_RECT.w, CANVAS_RECT.h))
        self.canvas.fill(CANVAS_BG)

        self.font = pygame.font.SysFont("arial", 15)
        self.small = pygame.font.SysFont("arial", 13)
        self._text_fonts = {}

        self.tool = tools.PENCIL
        self.color = (0, 0, 0)
        self.size_level = 2

        self.drawing = False          # mouse is down on the canvas
        self.start = None             # canvas coords where the drag began
        self.last = None              # previous mouse position (pencil / eraser)
        self.cursor = None            # current mouse position (canvas coords)
        self.textbox = None           # tools.TextBox while typing
        self.history = []             # undo stack of canvas copies
        self.message = ""
        self.message_until = 0

        self._build_ui()

    # ------------------------------------------------------------------ UI layout
    def _build_ui(self):
        self.tool_rects = [pygame.Rect(10 + i * 90, 8, 84, 34) for i in range(len(TOOL_BUTTONS))]
        self.palette_rects = [pygame.Rect(10 + i * 34, 52, 30, 30) for i in range(len(PALETTE))]
        self.size_rects = {lvl: pygame.Rect(580 + (lvl - 1) * 86, 52, 80, 30) for lvl in (1, 2, 3)}
        self.color_box = pygame.Rect(860, 48, 40, 38)

    @property
    def width(self):
        return tools.BRUSH_SIZES[self.size_level]

    # ------------------------------------------------------------------ helpers
    def to_canvas(self, pos):
        return (pos[0], pos[1] - TOOLBAR_H)

    def to_screen(self, pos):
        return (pos[0], pos[1] + TOOLBAR_H)

    def show_message(self, text):
        self.message = text
        self.message_until = pygame.time.get_ticks() + 3500

    def push_history(self):
        self.history.append(self.canvas.copy())
        if len(self.history) > 30:
            self.history.pop(0)

    def undo(self):
        self.textbox = None
        self.drawing = False
        if self.history:
            self.canvas = self.history.pop()
            self.show_message("Undo")

    def text_font(self):
        size = tools.TEXT_SIZES[self.size_level]
        if size not in self._text_fonts:
            self._text_fonts[size] = pygame.font.SysFont("arial", size)
        return self._text_fonts[size]

    def set_tool(self, tool):
        self.commit_text()
        self.drawing = False
        self.tool = tool

    # ------------------------------------------------------------------ text tool
    def commit_text(self):
        """Render the typed text permanently onto the canvas (Enter)."""
        box = self.textbox
        self.textbox = None
        if box is None or not box.content:
            return
        self.push_history()
        img = self.text_font().render(box.content, True, self.color)
        self.canvas.blit(img, box.pos)

    # ------------------------------------------------------------------ saving
    def save(self):
        """Ctrl+S: write the canvas to saves/paint_YYYYmmdd_HHMMSS.png"""
        self.commit_text()
        os.makedirs(SAVE_DIR, exist_ok=True)
        stamp = datetime.datetime.now().strftime("paint_%Y%m%d_%H%M%S")
        path = os.path.join(SAVE_DIR, stamp + ".png")
        n = 1
        while os.path.exists(path):               # two saves in the same second
            path = os.path.join(SAVE_DIR, "{}_{}.png".format(stamp, n))
            n += 1
        pygame.image.save(self.canvas, path)
        self.show_message("Saved " + os.path.relpath(path, BASE_DIR))

    # ------------------------------------------------------------------ events
    def handle_event(self, e):
        if e.type == pygame.KEYDOWN:
            self.on_key(e)
        elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            self.on_mouse_down(e.pos)
        elif e.type == pygame.MOUSEMOTION:
            self.on_mouse_move(e.pos)
        elif e.type == pygame.MOUSEBUTTONUP and e.button == 1:
            self.on_mouse_up(e.pos)

    def on_key(self, e):
        if e.mod & (pygame.KMOD_CTRL | pygame.KMOD_META):       # Ctrl (or Cmd on Mac)
            if e.key == pygame.K_s:
                self.save()
            elif e.key == pygame.K_z:
                self.undo()
            return

        if self.textbox is not None:                            # typing mode
            if e.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self.commit_text()
            elif e.key == pygame.K_ESCAPE:
                self.textbox = None                              # cancel
            elif e.key == pygame.K_BACKSPACE:
                self.textbox.content = self.textbox.content[:-1]
            elif e.unicode and e.unicode.isprintable():
                self.textbox.content += e.unicode
            return

        if e.key == pygame.K_ESCAPE:
            self.drawing = False
        elif e.key in SIZE_KEYS:
            self.size_level = SIZE_KEYS[e.key]
        else:
            for tool, _label, key in TOOL_BUTTONS:
                if e.key == ord(key):
                    self.set_tool(tool)
                    break

    def on_mouse_down(self, pos):
        if pos[1] < TOOLBAR_H:
            self.on_toolbar_click(pos)
            return
        cp = self.to_canvas(pos)
        t = self.tool

        if t == tools.TEXT:
            self.commit_text()                                   # finish the previous text first
            self.textbox = tools.TextBox(cp)
            return
        if t == tools.FILL:
            self.push_history()
            tools.flood_fill(self.canvas, cp, self.color)
            return
        if t == tools.PICKER:
            self.color = tuple(self.canvas.get_at(cp))[:3]
            return

        self.drawing = True
        self.start = self.last = self.cursor = cp
        if t == tools.PENCIL:
            self.push_history()
            tools.draw_dot(self.canvas, self.color, cp, self.width)
        elif t == tools.ERASER:
            self.push_history()
            tools.draw_dot(self.canvas, CANVAS_BG, cp, self.width * tools.ERASER_FACTOR)

    def on_mouse_move(self, pos):
        cp = self.to_canvas(pos)
        self.cursor = cp
        if not self.drawing:
            return
        if self.tool == tools.PENCIL:
            tools.draw_line(self.canvas, self.color, self.last, cp, self.width)
            self.last = cp
        elif self.tool == tools.ERASER:
            tools.draw_line(self.canvas, CANVAS_BG, self.last, cp, self.width * tools.ERASER_FACTOR)
            self.last = cp

    def on_mouse_up(self, pos):
        if not self.drawing:
            return
        self.drawing = False
        cp = self.to_canvas(pos)
        if self.tool in tools.SHAPE_TOOLS and cp != self.start:
            self.push_history()
            tools.draw_shape(self.canvas, self.tool, self.color, self.start, cp, self.width)

    def on_toolbar_click(self, pos):
        for rect, (tool, _label, _key) in zip(self.tool_rects, TOOL_BUTTONS):
            if rect.collidepoint(pos):
                self.set_tool(tool)
                return
        for rect, color in zip(self.palette_rects, PALETTE):
            if rect.collidepoint(pos):
                self.color = color
                return
        for level, rect in self.size_rects.items():
            if rect.collidepoint(pos):
                self.size_level = level
                return

    # ------------------------------------------------------------------ drawing
    def draw(self):
        self.screen.fill(PANEL)
        self.screen.blit(self.canvas, CANVAS_RECT.topleft)

        # live previews are drawn on the screen, clipped to the canvas area
        self.screen.set_clip(CANVAS_RECT)
        if self.drawing and self.tool in tools.SHAPE_TOOLS and self.cursor is not None:
            tools.draw_shape(self.screen, self.tool, self.color,
                             self.to_screen(self.start), self.to_screen(self.cursor), self.width)
        if self.textbox is not None:
            self.draw_text_preview()
        self.screen.set_clip(None)

        self.draw_toolbar()
        pygame.display.flip()

    def draw_text_preview(self):
        font = self.text_font()
        x, y = self.to_screen(self.textbox.pos)
        img = font.render(self.textbox.content, True, self.color)
        self.screen.blit(img, (x, y))
        if (pygame.time.get_ticks() // 500) % 2 == 0:             # blinking caret
            cx = x + img.get_width() + 1
            pygame.draw.line(self.screen, self.color, (cx, y), (cx, y + font.get_height()), 2)

    def draw_toolbar(self):
        pygame.draw.rect(self.screen, PANEL, (0, 0, WIDTH, TOOLBAR_H))
        pygame.draw.line(self.screen, BORDER, (0, TOOLBAR_H - 1), (WIDTH, TOOLBAR_H - 1), 2)

        for rect, (tool, label, key) in zip(self.tool_rects, TOOL_BUTTONS):
            self.draw_button(rect, label, tool == self.tool)

        for rect, color in zip(self.palette_rects, PALETTE):
            pygame.draw.rect(self.screen, color, rect)
            border = (255, 60, 60) if color == self.color else BORDER
            pygame.draw.rect(self.screen, border, rect, 3 if color == self.color else 1)

        for level, rect in self.size_rects.items():
            self.draw_button(rect, SIZE_LABELS[level], level == self.size_level)

        pygame.draw.rect(self.screen, self.color, self.color_box)
        pygame.draw.rect(self.screen, BORDER, self.color_box, 2)
        self.screen.blit(self.small.render("Color", True, TEXT_COLOR), (self.color_box.right + 8, 58))

        label = dict((t, l) for t, l, _k in TOOL_BUTTONS)[self.tool]
        status = "Tool: {}    Brush: {}px    RGB{}".format(label, self.width, self.color)
        self.screen.blit(self.font.render(status, True, TEXT_COLOR), (10, 90))
        if self.message and pygame.time.get_ticks() < self.message_until:
            msg = self.font.render(self.message, True, (20, 110, 40))
            self.screen.blit(msg, (560, 90))
        else:
            help_text = "1/2/3 size | Ctrl+S save | Ctrl+Z undo | Text: Enter = confirm, Esc = cancel"
            self.screen.blit(self.small.render(help_text, True, (70, 70, 85)), (560, 92))

    def draw_button(self, rect, label, active):
        pygame.draw.rect(self.screen, BTN_ACTIVE if active else BTN, rect, border_radius=5)
        pygame.draw.rect(self.screen, BORDER, rect, 1, border_radius=5)
        img = self.font.render(label, True, TEXT_COLOR)
        self.screen.blit(img, img.get_rect(center=rect.center))

    # ------------------------------------------------------------------ main loop
    def run(self):
        running = True
        while running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                else:
                    self.handle_event(e)
            self.draw()
            self.clock.tick(60)
        pygame.quit()


if __name__ == "__main__":
    PaintApp().run()
