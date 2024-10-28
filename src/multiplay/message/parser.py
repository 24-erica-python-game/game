from typing import List

from cmd_token import *
from src.game.rule import GameSystem
from tokenizer import Scanner


class MessageParser:
    def __init__(self, source: str, game: GameSystem):
        self.source = source
        self.source += ","
        self.game = game

    def parse(self) -> List[Identifier]:
        """
        주어진 소스를 파싱해 명령으로 변환함
        :return: 변환된 명령
        """
        scanner = Scanner(self.source)
        tokenized = scanner.tokenize()
        curr_cmd = None
        tokens = []
        for token in tokenized:
            if isinstance(token, Identifier):
                curr_cmd = token
                tokens.append(curr_cmd)
            else:
                try:
                    assert curr_cmd is not None
                except AssertionError:  # if curr_cmd is None;
                    raise AssertionError("""Expected instance of Identifier, got None.
                    The first argument must be instance of Identifier.""")
                else:
                    curr_cmd.args.append(token)
        return tokens

    def execute(self, command_list: List[Identifier]):
        """
        매개변수로 받은 명령을 실행함
        :param command_list: 명령 목록
        """
        for command in command_list:
            self.game.call_command(command.lexeme, command.args)

    def run(self):
        """
        소스를 파싱한 다음 명령을 실행함.

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
