import sys
from dataclasses import dataclass
from types import FunctionType
from typing import Optional, Self

from src.game.tile.types import Position
from src.game.unit.base import BaseUnit
from src.game.command import commands
from src.game.deck import Deck
from src.game.player import Player
from src.game.tile.base import BaseTile
from utils.game_logger import GameLogger, PlayerData


@dataclass
class GameRule:
    map_size: tuple[int, int]  # 맵 크기
    enable_fow: bool  # 전장의 안개
    start_ticket: int  # 시작시 주어지는 티켓의 값


class GameSystem:
    _instance: Optional[Self] = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(GameSystem, cls).__new__(cls)
        return cls._instance

    def __init__(self, ruleset: Optional[GameRule] = None) -> None:
        """
        :param ruleset: 게임 시스템을 초기화할 규칙, None일 경우 게임 시스템을 호출함
        :raises ValueError: `GameSystem` 이 초기화되지 않았으며 `ruleset` 이 None 일 경우
        """
        if not hasattr(self, '_initialized'):
            if ruleset is None:
                raise ValueError("ruleset must be provided when init.")

            self.ruleset = ruleset
            self.players: list[Optional[Player]] = [Player(f"P{i + 1}", ruleset.start_ticket, Deck()) for i in range(2)]
            self.current_turn = 0
            self.callable_commands: dict[str, FunctionType] = commands
            self.map_data: Optional[list[list[BaseTile]]] = None
            self._initialized = True
            self.logger = None

    # def init_game_logger(self):
    #     player_data = [PlayerData(name=player.nickname, number=p_idx)
    #                    for p_idx, player in enumerate(self.players)]
    #     self.logger = GameLogger(player_data)

    def switch_turn(self) -> int:
        """
        다음 플레이어로 턴을 넘기고, 현재 플레이어의 인덱스를 반환함.

        :return: 넘어간 플레이어의 인덱스
        """
        self.current_turn = (self.current_turn + 1) % len(self.players)

        if self.players[self.current_turn] is None:
            self.switch_turn()

        return self.current_turn

    def call_command(self, cmd_name: str, *args):
        """
        src/multiplay/commands/commands.py의 command 딕셔너리 변수에 있는 함수를 호출한다.

        먼저 함수를 인수와 함께 호출하며 만약 `TypeError` 가 발생할 경우 인수 없이 호출한다.

        :param cmd_name: 명령 이름
        :param args: 명령에 전달되는 인수
        :return:
        """
        try:
            self.callable_commands[cmd_name](*args)
        except TypeError:
            self.callable_commands[cmd_name]()
        except Exception as e:
            print(f"An error occured in function call_command:\n"
                  f"cmd_name: {cmd_name}\n"
                  f"{e}", file=sys.stderr)

    def check_win_condition(self) -> Optional[Player]:
        """
        승리 조건을 검사하고, 승리한 플레이어가 있다면 반환함.

        :return: 남은 플레이어가 1명이라면 그 플레이어를 반환하고, 아닐 경우 `None` 반환
        """
        num_players = 0
        idx = 0

        for p_idx, player in enumerate(self.players):
            if player is not None:
                num_players += 1
                idx = p_idx

        if num_players == 1:
            return self.players[idx]
        else:
            return None

    def check_all_players_tickets(self) -> list[tuple[int, Player]]:
        """
        모든 플레이어의 티켓을 검사하고, 티켓이 0 이하인 플레이어를 제거함.

        :return: 제거된 플레이어 목록, (플레이어 번호, 플레이어 인스턴스) 형태로 넘겨짐.
        """
        removed_players = []

        for p_num, player in enumerate(self.players):
            if player is not None:
                if player.ticket <= 0:
                    removed_players.append((p_num, player))
                    self.players[p_num] = None

        return removed_players

    def deploy_unit(self, unit: 'BaseUnit', pos: Position) -> None:
        """
        유닛을 배치하는 메서드

        :param unit:
        :param pos:
        :return:
        """
        self.map_data[pos.q][pos.r].place_unit(unit)

    def defeat_player(self, player: Player) -> None:
        """
        패배 메서드

        턴을 넘긴 후 플레이어 목록에서 해당 플레이어를 ``None`` 으로 바꿈.

        :param player:
        :return:
        """
        # player.ticket = 0
        p_idx = self.players.index(player)

        if self.current_turn == self.players.index(player):
            self.switch_turn()
            self.players[p_idx].ticket = None
