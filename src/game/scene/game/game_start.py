from game.scene.base import Scene


class GameEndScene(Scene):
    """
    맵을 확인하며 덱을 짜는 단계
    """
    def __init__(self):
        super().__init__("game.game_start")

    def run(self):
        pass
