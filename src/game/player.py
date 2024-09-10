from src.game.deck import Deck
from src.game.tile.types import Position
from src.game.unit.base import BaseUnit


class Player:
    def __init__(self, nickname: str, ticket: int, deck: Deck):
        self.nickname = nickname
        self.ticket = ticket
        self.deck = deck

    def place_unit(self, unit: BaseUnit, pos: Position):
        pass
