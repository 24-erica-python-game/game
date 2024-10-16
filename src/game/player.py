from src.game.deck import Deck
from src.game.tile.types import Position
from src.game.unit.base import BaseUnit

class Player: pass

class Player:
    def __init__(self, nickname: str, ticket: int, deck: Deck):
        self.nickname = nickname
        self.ticket = ticket
        self.deck = deck

    def deploy_unit(self, unit: BaseUnit, pos: Position) -> None:
        """
        유닛을 배치하는 메서드
        :param unit:
        :param pos:
        :return:
        """
        from src.game.rule import GameSystem
        GameSystem().map_data[pos.q][pos.r].place_unit(unit)

    def surrender(self) -> None:
        """
        항복 메서드

        티켓을 모두 제거하고 턴을 넘김
        :return:
        """
        from src.game.rule import GameSystem
        self.ticket = 0
        GameSystem().switch_turn()