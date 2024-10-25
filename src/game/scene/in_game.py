from game.scene.base import Scene
from game.tile.tile import MapManager


class GameScene(Scene):
    def __init__(self, map_name: str):
        self.tile_map = MapManager(map_name)
        super().__init__("game")

    def logic(self):
        pass

    def draw(self):
        pass

    def input(self):
        pass

    def run(self, *args, **kwargs):
        self.logic()
        self.draw()
        self.input()
