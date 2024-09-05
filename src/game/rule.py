from dataclasses import dataclass
from types import FunctionType

from src.game.player import Player
from src.multiplay.message.cmd_token import String, Number


@dataclass
class GameRule:
    map_size: tuple[int, int]  # 맵 크기
    enable_fow: bool           # 전장의 안개
    start_ticket: int          # 시작시 주어지는 티켓의 값


class GameSystem:
    def __init__(self, ruleset: GameRule) -> None:
        self.players = [ Player(f"P{i+1}", ruleset.start_ticket) for i in range(2) ]
        self.current_turn = 0
        self.callable_commands: dict[str, FunctionType] = dict()

    class register_command:  # decorator
        """
        self.callable_commands에 명령어를 등록하는 데코레이터

        선언 예시:

        >>> @register_command(name="exampleCmd")
        >>> def example_cmd(self, arg1: String, arg2: Number):
        >>>     ...

        :param name: 등록할 이름
        :param args: 함수에 전달할 인수
        """
        def __init__(self, name: str, *args):
            self.args = args

        def __call__(self, func):
            def wrapped_func(*args):
                func(*args)
            return wrapped_func


    def switch_turn(self) -> int:
        self.current_turn = (self.current_turn + 1) % len(self.players)

    def call(self, cmd_name: str, args):
        pass

    @register_command("test_cmd_1")
    def _call_test_without_arg(self):
        print("_call_test_no_arg called;")

    @register_command("test_cmd_2")
    def _call_test_with_arg(self, *args):
        print(f"_call_test_with_arg called;\nargs: {args}")
