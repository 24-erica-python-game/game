from types import FunctionType
from typing import List

from tokenizer import Scanner
from cmd_token import *
from src.game import command


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
        for command in command_list:
            self.game.call(command.lexeme, command.args)

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
msg_parser = MessageParser("_call_test_with_args:'arg1',500;", game_system)
l = msg_parser.parse()
msg_parser.run()
msg_parser = MessageParser("_call_test_without_args;", game_system)
msg_parser.run()
