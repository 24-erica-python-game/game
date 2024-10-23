import pygame as pg
from pygame import SurfaceType

from game.ui.templates.slider import Slider, SliderHead


scrollbar_width = 30

class ScrollBar(Slider):
    def __init__(self, surface: SurfaceType):
        surface.get_size()
        super().__init__()
