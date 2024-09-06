"""
문법:

identifier         ::= [A-Za-z_]*[A-Za-z0-9_]

number             ::= [1-9]*[0-9]

string             ::= "'" [A-Za-z0-9_]* "'"

argument           ::= (string | number)

command            ::= identifier ":" (argument,)* ";"
"""

from cmd_token import *


class Scanner:
    def __init__(self, source: str):
        self.source = source
        self.start = 0
        self.current = 0
        self.tokens = []

    def _peek(self) -> int:
        try:
            return ord(self.source[self.current])
        except IndexError:
            return 0

    def _substring(self):
        return self.source[self.start:self.current]

    def _is_ascii_alpha(self) -> bool:
        return (ord('A') <= self._peek() <= ord('Z')) or (ord('a') <= self._peek() <= ord('z'))

    def _is_numeric(self) -> bool:
        return ord('0') <= self._peek() <= ord('9')

    def _is_ascii_alphanumeric(self) -> bool:
        return self._is_ascii_alpha() or self._is_numeric()

    def _number(self):
        self.current += 1
        while True:
            if ord("0") <= self._peek() <= ord("9"):
                self.current += 1
            else:
                break
        return Number(self._substring())

    def _string(self):
        self.current += 1
        while True:
            if self._peek() == ord("'"):
                self.current += 1
                break
            elif self._peek() == ord("\0"):
                raise ValueError("Unterminated string")
            elif self._is_ascii_alphanumeric():
                self.current += 1
            else:
                raise ValueError("Unexpected character")
        return String(self._substring())

    def _identifier(self):
        self.current += 1
        while True:
            if self._is_ascii_alphanumeric() or \
                    self._peek() == ord('_'):
                self.current += 1
            else:
                if self._peek() == ord(':'):
                    break
                else:
                    break
        return Identifier(self._substring())

    def tokenize(self):
        while True:
            if self.current < len(self.source):
                self.start = self.current
            else:
                break

            # identifier
            if self._is_ascii_alpha() or self._peek() == ord('_'):
                token = self._identifier()
            # string
            elif self._peek() == ord('\''):
                token = self._string()
            # number
            elif self._peek() == ord(','):
                self.current += 1
                continue
            elif self._peek() == ord('\0'):
                break
            elif self._is_numeric():
                token = self._number()
            else:
                raise ValueError(f"Invalid character in {self.current}: {self.source[self.current]}")
            self.tokens.append(token)

            self.current += 1
        return self.tokens
