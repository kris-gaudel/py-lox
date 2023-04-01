from token_type import TokenType
#from lox import Lox
import Expr
import Stmt

class ParseError(RuntimeError):
    """An error has occurred!"""

class Parser:
    def __init__(self, tokens):
        self.current = 0
        self.tokens = tokens
        
    def expression(self):
        return self.assignment()
    
    def declaration(self):
        try:
            if (self.match(TokenType.VAR)):
                return self.var_declaration()
            return self.statement()
        except:
            #raise RuntimeError
            self.synchronize()
            return None

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
        return self.peek().type == type
    
    def advance(self):
        if (not self.is_at_end()):
            self.current += 1
        return self.previous()
    
    def is_at_end(self):
        return self.peek().type == TokenType.EOF
    
    def peek(self):
        return self.tokens[self.current]
    
    def previous(self):
        return self.tokens[self.current - 1]
    
    def comparison(self):
        expr = self.term()
        while (self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL)):
            operator = self.previous()
            right = self.term()
            expr = Expr.Binary(expr, operator, right)

        return expr
    
    def term(self):
        expr = self.factor()
        while (self.match(TokenType.MINUS, TokenType.PLUS)):
            operator = self.previous()
            right = self.factor()
            expr = Expr.Binary(expr, operator, right)
        
        return expr

    def factor(self):
        expr = self.unary()
        while(self.match(TokenType.SLASH, TokenType.STAR)):
            operator = self.previous()
            right = self.unary()
            expr = Expr.Binary(expr, operator, right)
        
        return expr

    def unary(self):
        if (self.match(TokenType.BANG, TokenType.MINUS)):
            operator = self.previous()
            right = self.unary()
            return Expr.Unary(operator, right)
        
        return self.primary()
    
    def primary(self):
        if (self.match(TokenType.FALSE)):
            return Expr.Literal(False)
        elif (self.match(TokenType.TRUE)):
            return Expr.Literal(True)
        elif (self.match(TokenType.NIL)):
            return Expr.Literal(None)
        elif (self.match(TokenType.NUMBER, TokenType.STRING)):
            return Expr.Literal(self.previous().literal)
        elif (self.match(TokenType.IDENTIFIER)):
            return Expr.Variable(self.previous())
        elif (self.match(TokenType.LEFT_PAREN)):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Expr.Grouping(expr)
        #return self.error(self.peek(), "Expect expression.")
        raise ParseError("Expect expression.")
        
    def consume(self, type, message):
        if (self.check(type)):
            return self.advance() 
        raise RuntimeError(message)

    def error(self, message):
        #Lox.error(token, message)
        raise RuntimeError(message)

    def synchronize(self):
        self.advance()
        while(not self.is_at_end()):
            if (self.previous().type == TokenType.SEMICOLON):
                return
            if (self.peek().type == TokenType.CLASS):
                return
            elif (self.peek().type == TokenType.FUN):
                return
            elif (self.peek().type == TokenType.VAR):
                return
            elif (self.peek().type == TokenType.FOR):
                return
            elif (self.peek().type == TokenType.IF):
                return
            elif (self.peek().type == TokenType.WHILE):
                return
            elif (self.peek().type == TokenType.PRINT):
                return
            elif (self.peek().type == TokenType.RETURN):
                return
        self.advance()
        
    def parse(self):
        statements = []
        while (not self.is_at_end()):
            statements.append(self.declaration())
        return statements
    
    def statement(self):
        if (self.match(TokenType.PRINT)):
            return self.print_statement()
        return self.expression_statement()
    
    def print_statement(self):
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Stmt.Print(value)
    
    def var_declaration(self):
        name = self.consume(TokenType.IDENTIFIER, "Expect variable name.")
        initalizer = None
        if (self.match(TokenType.EQUAL)):
            initalizer = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
        return Stmt.Var(name, initalizer)
    
    def expression_statement(self):
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return Stmt.Expression(expr)

    def assignment(self):
        expr = self.equality()
        if (self.match(TokenType.EQUAL)):
            equals = self.previous()
            value = self.assignment()
            if (isinstance(expr, Expr.Variable)):
                return Expr.Assign(expr.name, value)
            raise ParseError("Invalid assignment target.")
        return expr
        
