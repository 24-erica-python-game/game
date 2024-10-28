from typing import Literal

import pygame as pg

from game.scene.base import Scene
from game.ui.base import UIPosition, UISize
from game.ui.color import RGB
from game.ui.templates.button import Button
from game.ui.templates.textbox import TextBox
from utils import Font, Config


class HomeScene(Scene):
    def __init__(self):
        super().__init__("home")
        self.subscene: Literal["main", "settings", "join_game", "create_game"] = "main"

    def run(self, *args, **kwargs):
        display_size = pg.display.get_surface().get_size()

        match self.subscene:
            case "main":
                def on_settings_click(): self.subscene = "settings"
                def on_join_game_click(): self.subscene = "join_game"
                def on_create_game_click(): self.subscene = "create_game"

                # 게임 생성, 게임 참여, 설정 버튼이 있는 화면
                button = Button("test1",
                                Font.get_font("default", Config.get_config("font.fonts")),
                                UIPosition(display_size[0] / 2, display_size[1] / 2),
                                UISize(50, 20),
                                foreground=RGB(0, 0, 0),
                                background=RGB(160, 160, 160))
                button.on_click = on_settings_click  # 이 코드가 잘 작동하는지 테스트 필요함.
                button.update()
            case "create_game":
                # 호스트가 되어 상대와 연결될때까지 대기한 후, 모두 준비되면 게임 씬으로 전환
                textbox = TextBox(UIPosition(display_size[0] / 2, display_size[1] / 2),
                                  UISize(50, 20),
                                  Font.get_font("default", Config.get_config("font.fonts")),
                                  "create_game subscene")
                textbox.update()
            case "join_game":
                # 게스트가 되어 호스트 정보를 입력해 연결될때까지 대기한 후, 모두 준비되면 게임 씬으로 전환
                pass
            case "settings":
                # 설정 화면
                pass
