from dataclasses import dataclass
from types import FunctionType
from typing import Optional

from src.game.command import commands
from src.game.deck import Deck
from src.game.player import Player
from src.game.tile.base import BaseTile


@dataclass
class GameRule:
    map_size: tuple[int, int]  # 맵 크기
    enable_fow: bool  # 전장의 안개
    start_ticket: int  # 시작시 주어지는 티켓의 값


class GameSystem:
    _instance: Optional['GameSystem'] = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(GameSystem, cls).__new__(cls)
        return cls._instance

    def __init__(self, ruleset: Optional[GameRule] = None) -> None:
        if not hasattr(self, '_initialized'):
            if ruleset is None:
                raise ValueError("ruleset must be provided when init.")

            self.ruleset = ruleset
            self.players = [Player(f"P{i + 1}", ruleset.start_ticket, Deck()) for i in range(2)]
            self.current_turn = 0
            self.callable_commands: dict[str, FunctionType] = commands
            self.map_data: Optional[list[list[BaseTile]]] = None
            self._initialized = True

    def switch_turn(self) -> int:
        """
        다음 플레이어로 턴을 넘기고, 현재 플레이어의 인덱스를 반환함.
        :return: 넘어간 플레이어의 인덱스
        """
        self.current_turn = (self.current_turn + 1) % len(self.players)
        return self.current_turn

    def call(self, cmd_name: str, *args):
        try:
            self.callable_commands[cmd_name](*args)
        except TypeError:
            self.callable_commands[cmd_name]()

    def check_win_condition(self) -> Optional[Player]:
        """
        승리 조건을 검사하고, 승리한 플레이어가 있다면 반환함.

        :return: 남은 플레이어가 1명이라면 그 플레이어를 반환하고, 아닐 경우 `None` 반환
        """
        return None if len(self.players) == 1 else self.players[0]

    def check_all_players_tickets(self) -> None:
        """
        모든 플레이어의 티켓을 검사하고, 티켓이 0 이하인 플레이어를 제거함.
        """
        players = self.players.copy()

        for player in players:
            if player.ticket <= 0:
                self.players.remove(player)

    def register_map(self, map_data: list[list[BaseTile]]) -> list[list[BaseTile]]:
        """
        맵 데이터를 등록하고 등록된 맵 데이터를 반환함.
        :param map_data: 맵 데이터
        :return: 등록된 맵 데이터
        """
        self.map_data = map_data

        return self.map_data
