from game.scene.base import Scene


class GameEndScene(Scene):
    """
    게임 결과 화면
    """
    def __init__(self):
        super().__init__("game.game_end")

    def run(self):
        pass
