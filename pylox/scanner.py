from lox import Lox
from lox_token import LoxToken
from token_type import TokenType

class Scanner:
    def __init__(self, source) -> None:
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1

    def scan_tokens(self):
        print("TEST")
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        self.tokens.append(LoxToken(TokenType.EOF, "", None, self.line))
        return self.tokens

    def is_at_end(self):
        return self.current >= len(self.source)
    
    def scan_token(self):
        c = self.advance()
        if c == '(':
            self.add_token(TokenType.LEFT_PAREN)
        elif c == ')':
            self.add_token(TokenType.RIGHT_PAREN)
        elif c == '{':
            self.add_token(TokenType.LEFT_CURLY_BRACE)
        elif c == '}':
            self.add_token(TokenType.RIGHT_CURLY_BRACE)
        elif c == ',':
            self.add_token(TokenType.COMMA)
        elif c == '.':
            self.add_token(TokenType.DOT)
        elif c == '+':
            self.add_token(TokenType.PLUS)
        elif c == '-':
            self.add_token(TokenType.MINUS)
        elif c == ';':
            self.add_token(TokenType.SEMICOLON)
        elif c == '*':
            self.add_token(TokenType.STAR)
        elif c == '!':
            to_add = self.match('=') if TokenType.BANG_EQUAL else TokenType.BANG
            self.add_token(to_add)
        elif c == '=':
            to_add = self.match('=') if TokenType.EQUAL_EQUAL else TokenType.EQUAL
            self.add_token(to_add)
        elif c == '>':
            to_add = self.match('=') if TokenType.GREATER_EQUAL else TokenType.GREATER
            self.add_token(to_add)
        elif c == '<':
            to_add = self.match('=') if TokenType.LESS_EQUAL else TokenType.LESS
            self.add_token(to_add)
        elif c == '/':
            if (self.match('/')):
                while ((self.peek() != '\n') and (self.is_at_end() == False)):
                    self.advance()
            else:
                self.add_token(TokenType.SLASH)   
        elif c == '\n':
            self.line += 1   
        elif c == '"':
            self.string()      
        else:
            Lox.error(self.line, "Unexpected character.")

    def advance(self):
        self.current += 1
        return self.source[self.current - 1]

    def add_token(self, token_type):
        self.add_token_main(token_type, None)

    def add_token_main(self, token_type, literal):
        text = self.source[self.start:self.current]
        self.tokens.append(LoxToken(token_type, text, literal, self.line))

    def match(self, expected):
        if (self.is_at_end()):
            return False
        if (self.source[self.current] != expected):
            return False
        self.current += 1
        return True

    def peek(self):
        if (self.is_at_end()):
            return '\0'
        return self.source[self.current]

    def string(self):
        while (self.peek() != '"' and self.is_at_end() == False):
            if (self.peek() == '\n'):
                self.line += 1
            self.advance()
        if (self.is_at_end()):
            Lox.error(self.line, "Unterminated string.")
        self.advance()
        value = self.source[self.start + 1:self.current - 1]
        self.add_token(TokenType.STRING, value)
