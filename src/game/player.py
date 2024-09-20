from game.unit.base import BaseUnit
from game.tile.types import Position
from game.deck import Deck


class Player:
    def __init__(self, nickname: str, ticket: int, deck: Deck):
        self.nickname = nickname
        self.ticket = ticket
        self.deck = deck

    def deploy_unit(self, unit: BaseUnit, pos: Position):
        pass

    def surrender(self):
        self.ticket = 0