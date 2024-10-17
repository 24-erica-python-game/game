import re
from enum import Enum
from types import FunctionType
from typing import Literal, Optional

import pygame as pg
from pygame.font import FontType

from game.ui.base import UIPosition, UISize, UIAlignment
from game.ui.color import RGB
from game.ui.templates.textbox import TextBox


class InputPatternPreset(Enum):
    UNSIGNED_INT    = r"[+]?[0-9]*"
    UNSIGNED_FLOAT  = r"[+]?[0-9]*.[0-9]*"
    UNSIGNED_NUMBER = r"[+]?[0-9]*(.[0-9]*)?"
    SIGNED_INT      = r"[+-]?[0-9]*"
    SIGNED_FLOAT    = r"[+-]?[0-9]*.[0-9]*"
    SIGNED_NUMBER   = r"[+-]?[0-9]*(.[0-9]*)?"


class TextInput(TextBox):
    def __init__(self,
                 pos: UIPosition,
                 size: UISize,
                 font: FontType,
                 default_str: str,
                 placeholder: Optional[str],
                 pattern: Optional[str | InputPatternPreset],
                 color: RGB,
                 alignment: Literal[UIAlignment.left, UIAlignment.center, UIAlignment.right],
                 return_type: type,
                 condition: Optional[FunctionType | bool] = None,
                 *condition_args):
        super().__init__(pos, size, font, default_str, color, alignment)
        if isinstance(pattern, InputPatternPreset):
            self.pattern: str = pattern.value()
        else:
            self.pattern: str = pattern
        self.return_type = return_type
        self.condition = condition
        self.condition_args = condition_args
        self.focused = False
        self.focused_time = 0
        self.blink_duration = 120
        self.cursor_color = RGB(100, 100, 100)
        self.placeholder = placeholder
        self.placeholder_color = RGB(220, 220, 220)

    def set_text(self, text: str):
        if hasattr(self.condition, '__call__'):
            result = self.condition(self.condition_args)
        else:
            result = self.condition

        pattern = re.compile(self.pattern)
        if pattern.match(text):
            if result:
                self.label = text

    def get_value(self):
        return self.return_type(self.label)

    def render(self):
        display = pg.display.get_surface()
        pos = self.pos
        text = self.font.render(self.label, True, self.color)
        label_pos_x = 0

        super().render()

        if self.focused:
            self.focused_time += 1
            if 0 <= self.focused_time % self.blink_duration <= (self.blink_duration // 2):
                pg.draw.aaline(display, self.cursor_color,
                               (self.pos.x + text.get_size()[0], self.pos.y),
                               (self.pos.x + text.get_size()[0], self.pos.y + text.get_size()[1]))
        elif self.label == "":
                text = self.font.render(self.placeholder, True, self.placeholder_color)

        display.blit(text, (label_pos_x, pos.y))


if __name__ == "__main__":
    import utils
    from game.ui.color import Color
    from utils.mouse import double_click

    pg.init()

    small_font = pg.font.SysFont("malgungothic", 14, False, False)

    # 화면 크기 지정
    size = (400, 300)
    screen = pg.display.set_mode(size)

    pg.display.set_caption("Buggy Buddies")

    # FPS 관련 설정
    running = True
    clock = pg.time.Clock()

    textinput = TextInput(UIPosition(170, 140),
                          UISize(60, 20),
                          small_font,
                          "default_str",
                          "placeholder",
                          None,
                          RGB(0, 0, 0),
                          UIAlignment.left,
                          object)

    while running:
        screen.fill(Color.WHITE)
        clock.tick(60)
        double_click()

        for event in pg.event.get():
            match event.type:
                case pg.QUIT:
                    running = False
                case utils.mouse.event_double_clicked:
                    if textinput.is_mouse_in_area():
                        textinput.focused = True
                        print("focused in")
                case pg.MOUSEBUTTONDOWN:
                    if not textinput.is_mouse_in_area():
                        textinput.focused = False
                        print("focused out")

        textinput.render()

        pg.display.flip()
