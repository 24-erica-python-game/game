
from abc import ABCMeta, abstractmethod

class Tile(ABCMeta):
    def __init__(self):
        # self.tile_type = tile_type
        pass

    @abstractmethod
    def on_arrived(self):
        pass

