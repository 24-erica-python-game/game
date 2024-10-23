from game.scene.base import Scene
from game.tile.tile import TileMap


class GameScene(Scene):
    def __init__(self, map_name: str):
        super().__init__("game")
        self.tile_map = TileMap(map_name)

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
