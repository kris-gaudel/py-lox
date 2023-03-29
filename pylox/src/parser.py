from token_type import TokenType
import Expr

class Parser:
    def __init__(self, tokens):
        self.current = 0
        self.tokens = tokens
        
    def expression(self):
        return self.equality()

    def equality(self):
        expr = self.comparison()

        while (self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL)):
            operator = self.previous()
            right = self.comparison()
            expr = Expr.Binary(expr, operator, right)
        return expr

    def match(self, *types):
        for type in types:
            if (self.check(type)):
                self.advance()
                return True
        return False

    def check(self, type):
        if (self.is_at_end()):
            return False
        return self.peek() == type
    
    def advance(self):
        if (self.is_at_end() == False):
            self.current += 1
        return self.previous()
    
    def is_at_end(self):
        return self.peek() == TokenType.EOF
    
    def peek(self):
        return self.tokens[self.current]
    
    def previous(self):
        return self.tokens[self.current - 1]