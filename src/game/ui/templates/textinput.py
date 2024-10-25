import re
from enum import Enum
from typing import Optional

import pygame as pg
from pygame.font import FontType

from game.ui.base import UIPosition, UISize
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
    """
    텍스트 입력 상자 템플릿.
    """
    def __init__(self,
                 pos: UIPosition,
                 size: UISize,
                 font: FontType,
                 default_str: str,
                 *,
                 placeholder: Optional[str] = None,
                 pattern: Optional[str | InputPatternPreset] = None):
        """
        :param pos:
        :param size:
        :param font:
        :param default_str:
        :param placeholder: (keyword-only)
        :param pattern: (keyword-only)
        """
        super().__init__(pos, size, font, default_str)
        if isinstance(pattern, InputPatternPreset):
            self.pattern: str = pattern.value()
        else:
            self.pattern: str = pattern
        self.focused = False
        self.focused_time = 0
        self.blink_duration = 120
        self.cursor_color = RGB(100, 100, 100)
        self.placeholder = placeholder
        self.placeholder_color = RGB(220, 220, 220)

    def set_text(self, text: str):
        """
        텍스트박스의 내용을 설정함.

        만약 ``pattern`` 필드가 ``None`` 이 아닐 경우 텍스트박스의 내용이 정규식에 대입해 참일 경우 해당 내용으로 변경함.
        :param text:
        :return:
        """
        pattern = re.compile(self.pattern)
        if pattern.match(text):
            self.label = text

    def get_text(self) -> str:
        """
        텍스트박스의 내용을 반환함.
        :return:
        """
        return self.label

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
                          placeholder="placeholder")

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
