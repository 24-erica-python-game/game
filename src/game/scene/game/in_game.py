import math
import os

import pygame as pg
from perlin_noise import PerlinNoise
from pygame import SurfaceType

from game.scene.base import Scene
from game.tile.base import BaseTile
from game.tile.tile import MapManager

type t_position = list[int]


class GameScene(Scene):
    """
    게임이 진행되는 단계
    """
    def _load_sprites(self):
        sprite_root_dir = "assets\\sprites\\maps"
        # TODO: threading 모듈로 로딩 속도 개선
        for sprite_dir in os.listdir(sprite_root_dir):
            for file in os.listdir(f"{sprite_root_dir}\\{sprite_dir}"):
                if file.endswith(".png") and not file.startswith("_"):
                    if file[:-4].endswith("under"):
                        sprite_size = (36, 41)
                    else:
                        sprite_size = (36, 47)

                    surf = pg.image.load(f"{sprite_root_dir}\\{sprite_dir}\\{file}")
                    self.sprites[file[:-4]] = (surf, sprite_size)
        print(self.tile_map)

        for i in range(len(self.tile_map)):
            for j in range(len(self.tile_map[0])):
                print(f"Tile({i}, {j}):\n"
                      f"    structure : {self.tile_map[i][j].placed_structure}\n"
                      f"    unit      : {self.tile_map[i][j].placed_unit}\n"
                      f"    tile_name : {self.tile_map[i][j].type_name}\n")

        print(self.sprites)

    def __init__(self, map_name: str):
        type img_data = SurfaceType
        type img_size = tuple[int, int]

        super().__init__("game.in_game")

        self.tile_map: list[list[BaseTile]] = MapManager().set_map(map_name)
        if self.tile_map is None:
            raise ValueError("Map not found")
        self.zoom_level = 0.0
        self.cam_pos: t_position = [0, 0]
        self.draw_distance = 2160
        self.sprites: dict[str, tuple[img_data, img_size]] = dict()
        self.noise = PerlinNoise(octaves=250)
        self.tile_size = (36, 41)

        self._load_sprites()

    def get_tile_sprite(self, tile: BaseTile, under: bool = False) -> SurfaceType:
        match tile.type_name:
            case "field":
                sprite_name = "field"
                num_variation = 3
            case "hill":
                sprite_name = "hill"
                num_variation = 3
            case "mountain":
                sprite_name = "mountain"
                num_variation = 3
            case "pond":
                sprite_name = "pond"
                num_variation = 3
            case _:
                sprite_name = "field"
                num_variation = 1

        rand_result = int(
            (abs(self.noise.noise([tile.position.q / 100, tile.position.r / 100])) * 125) % num_variation + 1)
        sprite_name = f"{sprite_name}_{rand_result}"

        if under:
            sprite_name += "_under"

        result_data = self.sprites[f"{sprite_name}"]

        return result_data[0]

    def draw_tile(self):
        screen = pg.display.get_surface()
        screen.fill((0, 0, 0))

        def x(x: int, y: int):
            return 16 + self.tile_size[0] * x + (y % 2 * (self.tile_size[0] / 2)) + self.cam_pos[0]

        def y(x: int):
            return 21 + math.ceil(self.tile_size[1] * 0.75) * x + 1 + self.cam_pos[1]

        map_size = (len(self.tile_map), len(self.tile_map[0]))

        for i in range(map_size[1] - 1):
            tile_l = self.get_tile_sprite(self.tile_map[i][0], under=True)
            tile_r = self.get_tile_sprite(self.tile_map[i][-1], under=True)
            screen.blit(tile_l, (x(0, i), y(i)))
            screen.blit(tile_r, (x(map_size[0] - 1, i), y(i)))

        for i in range(map_size[0]):
            tile_bottom = self.get_tile_sprite(self.tile_map[-1][i], under=True)
            screen.blit(tile_bottom, (x(i, map_size[1] - 1), y(map_size[1] - 1)))

        for i in range(map_size[1] - 1):
            for j in range(1, map_size[0] - 1):
                tile = self.get_tile_sprite(self.tile_map[i][j])
                screen.blit(tile, (x(j, i), y(i)))

    def set_cam(self):
        keys = pg.key.get_pressed()
        multiplier = 8
        for _ in range(multiplier):
            self.cam_pos[0] += (keys[pg.K_LEFT] - keys[pg.K_RIGHT])
            self.cam_pos[1] += (keys[pg.K_UP] - keys[pg.K_DOWN])

        rel = pg.mouse.get_rel()

        if pg.mouse.get_pressed()[0]:
            self.cam_pos[0] += rel[0]
            self.cam_pos[1] += rel[1]

    def run(self, *args, **kwargs):
        self.set_cam()
        self.draw_tile()
