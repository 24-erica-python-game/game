from typing import Optional, Callable, Any

from pygame.font import FontType

from game.ui.base import UIPosition, UISize
from game.ui.templates.textbox import TextBox


class TextInput(TextBox):
    """
    텍스트 입력 상자 템플릿.
    """
    def __init__(self,
                 pos: UIPosition,
                 size: UISize,
                 font: FontType,
                 label: str,
                 *,
                 validator: Callable[[Any], bool] = lambda _: True):
        super().__init__(pos, size, font, label)
        self.textinput_manager = pg_textinput.TextInputManager(initial=label,
                                                               validator=validator)
        self.textinput_visualizer = pg_textinput.TextInputVisualizer(self.textinput_manager,
                                                                     self.font,
                                                                     True,
                                                                     self.color)

    def update(self):
        self.label = self.textinput_manager.value

        self.textinput_visualizer.update(pg.event.get())
        super().update()
        pg.display.get_surface().blit(self.textinput_visualizer.surface, self.pos)


if __name__ == "__main__":
    import pygame_textinput as pg_textinput
    import pygame as pg
    import utils
    from game.ui.color import Color
    from utils.mouse import double_click

    pg.init()

    small_font = pg.font.SysFont("malgungothic", 14, False, False)

    # 화면 크기 지정
    size = (400, 300)
    screen = pg.display.set_mode(size)

    pg.display.set_caption("Buggy Buddies")

    textinput = TextInput(UIPosition(200, 100), UISize(50, 20), small_font, "test")

    # FPS 관련 설정
    running = True
    clock = pg.time.Clock()

    pg.key.set_repeat(500, 50)

    while running:
        screen.fill(Color.WHITE)
        clock.tick(60)

        events = pg.event.get()
        textinput.update()

        for event in events:
            match event.type:
                case pg.QUIT:
                    running = False
                case utils.mouse.event_double_clicked:
                    pass
                case pg.MOUSEBUTTONDOWN:
                    pass

        pg.display.flip()
