from game.scene import Scene
from game.tile.tile import TileMap


class InGame(Scene):
    def __init__(self, map_name: str):
        super().__init__()
        self.tile_map = TileMap(map_name)

    def main_loop(self):
        while True:
            pass

    def draw_ui(self):
        pass

    def handle_input(self):
        pass

    def run(self):
        self.main_loop()
        self.draw_ui()
        self.handle_input()
