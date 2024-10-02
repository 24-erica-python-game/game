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
                 pattern: str | InputPatternPreset,
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
        text_size = UISize(text.get_size()[0], text.get_size()[1])
        label_pos_x = 0

        match self.alignment:
            case UIAlignment.left:
                label_pos_x = pos.x
            case UIAlignment.center:
                label_pos_x = pos.x + (self.size[0] - text_size.x) / 2
            case UIAlignment.right:
                label_pos_x = pos.x + (self.size[0] - text_size.x)

        if self.focused:
            self.focused_time += 1
            if 0 <= self.focused_time % self.blink_duration <= (self.blink_duration // 2):
                pg.draw.aaline(display, self.cursor_color,
                               (self.pos.x + text.get_size()[0], self.pos.y),
                               (self.pos.x + text.get_size()[0], self.pos.y + text.get_size()[1]))
        elif self.label == "":
                text = self.font.render(self.placeholder, True, self.placeholder_color)

        display.blit(text, (label_pos_x, pos.y))
