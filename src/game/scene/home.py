from typing import Literal

from game.scene.base import Scene


class HomeScene(Scene):
    def __init__(self):
        super().__init__("home")
        self.subscene: Literal["main", "settings", "join_game", "create_game"] = "main"

    def run(self, *args, **kwargs):
        match self.subscene:
            case "main":
                # 게임 생성, 게임 참여, 설정 버튼이 있는 화면
                pass
            case "create_game":
                # 호스트가 되어 상대와 연결될때까지 대기한 후, 모두 준비되면 게임 씬으로 전환
                pass
            case "join_game":
                # 게스트가 되어 호스트 정보를 입력해 연결될때까지 대기한 후, 모두 준비되면 게임 씬으로 전환
                pass
            case "settings":
                # 설정 화면
                pass
