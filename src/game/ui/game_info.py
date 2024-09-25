import pygame as pg

from src.game.ui.base import UI, UIPosition, UISize
from src.utils.config import Config
from src.game.ui.color import Color


class GameInfo(UI):
    def __init__(self):
        self.enemy_unit = None
        self.player_unit = None
        self.player_ticket = None
        self.turn_count = None

        self.font = pg.font.SysFont(Config.get_config("font.default_font"),
                                    Config.get_config("font.default_size"))
        self.position = UIPosition(640, 10)
        self.size = UISize(1280, 50)

        self.rect = (self.position.x, self.position.y,
                     self.size.x,     self.size.y)

    def render(self,
               enemy_unit: int,
               player_unit: int,
               player_ticket: int,
               turn_count: int):
        self.enemy_unit = enemy_unit
        self.player_unit = player_unit
        self.player_ticket = player_ticket
        self.turn_count = turn_count

        screen = pg.display.get_surface()

        game_info = self.font.render("게임 정보", True, Color.BLACK)
        enemy_unit = self.font.render(f"남은 적 유닛: {self.enemy_unit}", True, Color.BLACK)
        player_unit = self.font.render(f"남은 아군 유닛: {self.player_unit}", True, Color.BLACK)
        ticket = self.font.render(f"남은 티켓: {self.player_ticket}", True, Color.BLACK)
        turn_count = self.font.render(f"현재 턴 수: {self.turn_count}", True, Color.BLACK)
        # deck_info = self.font.render(f"덱 정보: {self.deck_info}", True, Color.BLACK)

        pg.draw.rect(screen, Color.GREEN, self.rect)
        screen.blit(game_info, (640, 10))
