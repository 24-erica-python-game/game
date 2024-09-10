from unit.base import BaseUnit
from tile.types import Position
from game.deck import Deck


class Player:
    def __init__(self, nickname: str, ticket: int, deck: Deck):
        self.nickname = nickname
        self.ticket = ticket
        self.deck = deck

    def place_unit(self, unit: BaseUnit, pos: Position):
        pass
