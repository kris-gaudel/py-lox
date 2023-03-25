class LoxToken:
    def __init__(self, type, lexeme, literal, line):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self) -> str:
        return f'{self.type}: {self.lexeme}, {self.literal}, {self.line}'

    def __repr__(self) -> str:
        properties = f'{self.type}, {self.lexeme}, {self.literal}, {self.line}'
        return f'{self.__class__.__name__}({properties})'