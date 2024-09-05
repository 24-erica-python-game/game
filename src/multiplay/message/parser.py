from types import FunctionType
from typing import List

from tokenizer import Scanner
from cmd_token import *


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
    game_system = None

    def __init__(self, name: str, *args):
        self.args = args
        self.name = name

    def __call__(self, func):
        if register_command.game_system is not None:
            register_command.callable_commands.update({self.name: func})
        else:
            pass

        def wrapped_func(*args):
            func(*args)

        return wrapped_func

    @staticmethod
    def set_game_system(game_system):
        register_command.game_system = game_system


# 테스트용 임시 클래스
class GameSystem:
    def __init__(self) -> None:
        self.current_turn = 0
        self.callable_commands: dict[str, FunctionType] = dict()

    def call(self, cmd_name: str, args):
        self.callable_commands[cmd_name](*args)

    @register_command("test_cmd_1")
    def _call_test_without_arg(self):
        print("_call_test_no_arg called;")

    @register_command("test_cmd_2")
    def _call_test_with_arg(self, *args):
        print(f"_call_test_with_arg called;\nargs: {args}")


class MessageParser:
    def __init__(self, source: str, game: GameSystem):
        self.source = source
        self.source += ","
        self.game = game

    def parse(self) -> List[Identifier]:
        scanner = Scanner(self.source)
        tokenized = scanner.tokenize()
        curr_cmd = None
        tokens = []
        for token in tokenized:
            print(f"token type: {type(token)} | {isinstance(token, Identifier)}")
            if isinstance(token, Identifier):  # False
                # id(token.__class__) == 2723135292032
                # id(Identifier) == 2723135266240
                curr_cmd = token
                tokens.append(curr_cmd)
            else:
                try:
                    assert curr_cmd is not None
                except AssertionError:  # if curr_cmd is None;
                    raise AssertionError("""
                    Expected instance of Identifier, got None.
                    The first argument must be instance of Identifier.
                    """)
                else:
                    curr_cmd.args.append(token)
        return tokens

    def execute(self, command_list: List[Identifier]):
        pass

    def run(self):
        """
        >>> msg_parser = MessageParser("...")
        >>> l = msg_parser.parse()
        >>> msg_parser.execute(l)
        위 코드는

        >>> msg_parser = MessageParser("...")
        >>> msg_parser.run()
        과 같음
        """
        commands = self.parse()
        self.execute(commands)


game_system = GameSystem()
register_command.set_game_system(game_system)

msg_parser = MessageParser("test_cmd_2:'arg1',500;", game_system)
msg_parser.run()
msg_parser = MessageParser("test_cmd_1;", game_system)
msg_parser.run()
