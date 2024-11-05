import pygame as pg
from pygame.sprite import Sprite

from game.ui.color import RGB


class Tile(Sprite):
    def __init__(self, pos, size, tile_data, sprite: tuple[str, bytes]):
        Sprite.__init__(self)
        self.pos = pos
        self.size = size
        self.tile_data = tile_data
        self.sprite = {
            "name": sprite[0],
            "image": pg.image.load(sprite[1]).convert_alpha()
        }

    def is_clicked(self) -> bool:
        """
        육각 타일이 클릭되었는지를 반환함.
        :return: 타일이 클릭되었을 경우 ``True``, 아닐 경우 ``False``.
        """
        pass

    def update(self, test: bool = False):
        """
        타일을 그림.
        :return:
        """
        pg.display.get_surface().blit(self.sprite["image"], self.pos)
        if test:
            pg.gfxdraw.rect(pg.display.get_surface(), RGB(255, 0, 0),
                            ((self.pos[0] - self.size[0] / 2, self.pos[1] - self.size[1] / 2),
                              self.size))
