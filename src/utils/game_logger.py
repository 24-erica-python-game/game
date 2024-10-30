import os
import sys
from dataclasses import dataclass
from typing import TextIO, Optional


log_path = os.path.normpath(f"{os.getcwd()}/data")


@dataclass
class PlayerData:
    name: str
    number: int


class GameLogger:

    """
    게임의 내용을 기록하는 로그를 생성함.

    로그는 텍스트 파일로 읽을 수 있도록 저장됨.
    """
    def __init__(self, player_data: list[PlayerData]):
        """
        :param player_data: 플레이어 데이터 목록, 정렬된 상태로 넘겨져야 함.
        """
        self.stream: Optional[TextIO] = None
        self.players = player_data
        self.indent = 0

    def new(self, filename: str):
        """
        새 게임 기록을 생성함.

        로그를 읽거나 쓰려면 먼저 이 메서드를 호출해야 함.

        :param filename: 로그의 이름. 마지막의 확장자는 생략해야 함.
        :return:
        """
        try:
            self.stream = open(f"{log_path}/{filename}.txt", "a")
        except OSError as e:
            self.stream = None
            print(f"failed to open file: {e}", file=sys.stderr)

    def write(self, content: str):
        """
        로그에 내용을 기록함

        :return:
        """
        if self.stream is not None:
            new_content = self.stream.readlines()
            new_content.append(" " * self.indent + content)
            self.stream.writelines(new_content)

    def set_indent(self, level: int):
        """
        로그의 들여쓰기 수준을 설정함.

        :param level: 들여쓰기 수준, 숫자 1당 공백 1개
        :return:
        """
        self.indent = level

    def close(self):
        """
        게임 기록 파일 스트림을 닫음.

        게임이 끝난 후 이 메서드를 호출해서 자원을 반납해야 함.

        :return:
        """
        if self.stream is not None:
            self.stream.close()
            self.stream = None

    def __del__(self):
        if self.stream is not None:
            try:
                self.close()
            except IOError:
                self.stream = None
