from typing import Literal

from pygame import gfxdraw as gfx

from game.ui.base import UIPosition, UISize
from game.ui.color import RGB
from game.ui.templates.interactable import Interactable


class CheckBox(Interactable):
    def __init__(self,
                 default_state: bool,
                 active_color: RGB,
                 active_indicator_type: Literal["square", "cross"],
                 pos: UIPosition,
                 size: UISize):
        self.state = default_state
        self.active_color = active_color
        self.active_indicator_type = active_indicator_type
        super().__init__(pos, size)

    def render(self):
        display = pg.display.get_surface()
        gfx.rectangle(display, (self.pos, self.size), RGB(70, 70, 70))

        if self.state:
            match self.active_indicator_type:
                case "square":
                    pg.draw.rect(display, self.active_color,
                                 (self.pos.x + 2, self.pos.y + 2,
                                  self.size.x - 4, self.size.y - 4))
                case "cross":
                    pg.draw.aaline(display, self.active_color,
                                   (self.pos.x + 2, self.pos.y + 2),
                                   (self.pos.x + self.size.x - 3, self.pos.y + self.size.y - 3))
                    pg.draw.aaline(display, self.active_color,
                                   (self.pos.x + 2, self.pos.y + self.size.y - 3),
                                   (self.pos.x + self.size.x - 3, self.pos.y + 2))

    def toggle_state(self) -> bool:
        """
        체크박스의 상태를 바꿔 다시 렌더링한 뒤, 바뀐 상태를 반환한다.

        :return: 체크박스의 최종 상태
        """
        self.state = not self.state
        self.render()

        return self.state


if __name__ == "__main__":
    import pygame as pg

    from game.ui.color import Color

    pg.init()

    small_font = pg.font.SysFont("malgungothic", 14, False, False)

    # 화면 크기 지정
    size = (400, 300)
    screen = pg.display.set_mode(size)

    pg.display.set_caption("Buggy Buddies")

    # FPS 관련 설정
    running = True
    clock = pg.time.Clock()

    checkbox = CheckBox(True, RGB(25, 25, 25), "cross", UIPosition(195, 145), UISize(10, 10))

    while running:
        screen.fill(Color.WHITE)
        clock.tick(30)

        for event in pg.event.get():
            match event.type:
                case pg.QUIT:
                    running = False
                case pg.MOUSEBUTTONDOWN if checkbox.is_mouse_in_area():
                    checkbox.toggle_state()

        checkbox.render()

        pg.display.flip()
