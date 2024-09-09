import pygame

from src.baseclasses.ui.ui import UI


class UnitInfo(UI):
    def __init__(self):
        self.font = pygame.font.SysFont('malgungothic', 18)
