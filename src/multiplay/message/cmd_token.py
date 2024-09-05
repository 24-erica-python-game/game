class Token:
    def __init__(self, lexeme):
        self.lexeme = lexeme
        print("token")


class String(Token):
    def __init__(self, lexeme):
        super().__init__(lexeme)
        print("string")


class Number(Token):
    def __init__(self, lexeme):
        super().__init__(lexeme)
        print("number")


class Identifier(Token):
    def __init__(self, lexeme):
        super().__init__(lexeme)
        self.command = lexeme.split(':')[0]
        self.args = []
        print("identifier")
