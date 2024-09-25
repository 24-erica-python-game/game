from dataclasses import dataclass
from types import FunctionType
from typing import Optional

from game.deck import Deck
from game import command
from game.player import Player


@dataclass
class GameRule:
    map_size: tuple[int, int]  # 맵 크기
    enable_fow: bool           # 전장의 안개
    start_ticket: int          # 시작시 주어지는 티켓의 값


class GameSystem:
    def __init__(self, ruleset: GameRule) -> None:
        self.players = [ Player(f"P{i+1}", ruleset.start_ticket, Deck()) for i in range(2) ]
        self.current_turn = 0
        self.callable_commands: dict[str, FunctionType] = command.commands

    def switch_turn(self) -> int:
        self.current_turn = (self.current_turn + 1) % len(self.players)

    def call(self, cmd_name: str, *args):
        try:
            self.callable_commands[cmd_name](*args)
        except TypeError:
            self.callable_commands[cmd_name]()

    def check_win_condition(self) -> Optional[Player]:
        """
        남은 플레이어가 1명뿐이라면 남은 플레이어를 반환하고, 아닐 경우 `None` 반환
        """
        return None if len(self.players) == 1 else self.players[0]

    def check_all_players_tickets(self) -> None:
        """
        | 현재 게임중인 플레이어들의 티켓을 검사하고,
        | 티켓이 0 이하로 떨어질 경우 게임에서 제거함.
        """
        players = self.players.copy()

        for player in players:
            if player.ticket <= 0:  # if not player.ticket으로 쓸 수 있지만 비직관적이어서 이 조건으로 둠.
                self.players.remove(player)
