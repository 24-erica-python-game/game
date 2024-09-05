class Token:
    def __init__(self, lexeme):
        self.lexeme = lexeme


class String(Token):
    def __init__(self, lexeme):
        super().__init__(lexeme)


class Number(Token):
    def __init__(self, lexeme):
        super().__init__(lexeme)


class Identifier(Token):
    def __init__(self, lexeme):
        super().__init__(lexeme)
        self.command = lexeme.split(':')[0]
        self.args = []
