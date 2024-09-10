from dataclasses import dataclass
from types import FunctionType

from deck import Deck
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
