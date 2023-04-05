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
            if (self.match(TokenType.FUN)):
                return self.function("function")
            if (self.match(TokenType.VAR)):
                return self.var_declaration()
            if (self.match(TokenType.CLASS)):
                return self.class_declaration()
            return self.statement()
        except:
            #raise RuntimeError
            self.synchronize()
            return None
        
    def class_declaration(self):
        name = self.consume(TokenType.IDENTIFIER, "Expect a class name.")
        super_class = None
        if (self.match(TokenType.LESS)):
            self.consume(TokenType.IDENTIFIER, "Expect superclass name.")
            super_class = Expr.Variable(self.previous())
        self.consume(TokenType.LEFT_BRACE, "Expect a '{' before class body.")
        methods = []
        while (not self.check(TokenType.RIGHT_BRACE)):
            methods.append(self.function("method"))
        self.consume(TokenType.RIGHT_BRACE, "Expect a '}' after class body.")
        return Stmt.Class(name, super_class, methods)

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
        
        return self.call()
    
    def finish_call(self, callee):
        arguments = []
        if (not self.check(TokenType.RIGHT_PAREN)):
            while self.match(TokenType.COMMA):
                if (len(arguments) >= 255):
                    raise ValueError("Can't have more than 255 arguments.")
                arguments.append(self.expression())
        paren = self.consume(TokenType.RIGHT_PAREN, "Expect ')' after arguments.")
        return Expr.Call(callee, paren, arguments)
    
    def call(self):
        expr = self.primary()
        while True:
            if (self.match(TokenType.LEFT_PAREN)):
                expr = self.finish_call(expr)
            elif (self.match(TokenType.DOT)):
                name = self.consume(TokenType.IDENTIFIER, "Expect property name after '.'.")
                expr = Expr.Get(expr, name)
            else:
                break
        return expr
    
    def primary(self):
        if (self.match(TokenType.FALSE)):
            return Expr.Literal(False)
        elif (self.match(TokenType.TRUE)):
            return Expr.Literal(True)
        elif (self.match(TokenType.NIL)):
            return Expr.Literal(None)
        elif (self.match(TokenType.NUMBER, TokenType.STRING)):
            return Expr.Literal(self.previous().literal)
        elif (self.match(TokenType.SUPER)):
            keyword = self.previous()
            self.consume(TokenType.DOT, "Expect '.' after 'super'.")
            method = self.consume(TokenType.IDENTIFIER, "Expect superclass method name.")
            return Expr.Super(keyword, method)
        elif (self.match(TokenType.THIS)):
            return Expr.This(self.previous())
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
        elif (self.match(TokenType.LEFT_BRACE)):
            return Stmt.Block(self.block())
        elif (self.match(TokenType.IF)):
            return self.if_statement()
        elif (self.match(TokenType.RETURN)):
            return self.return_statement()
        elif (self.match(TokenType.WHILE)):
            return self.while_statement()
        elif (self.match(TokenType.FOR)):
            return self.for_statement()
        return self.expression_statement()
    
    def if_statement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after 'if' condition.")
        then_branch = self.statement()
        else_branch = None
        if (self.match(TokenType.ELSE)):
            else_branch = self.statement()
        return Stmt.If(condition, then_branch, else_branch)
    
    def print_statement(self):
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Stmt.Print(value)
    
    def return_statement(self):
        keyword = self.previous()
        value = None
        if (not self.check(TokenType.SEMICOLON)):
            value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after return value.")
        return Stmt.Return(keyword, value)
    
    def var_declaration(self):
        name = self.consume(TokenType.IDENTIFIER, "Expect variable name.")
        initializer = None
        if (self.match(TokenType.EQUAL)):
            initializer = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
        return Stmt.Var(name, initializer)
    
    def while_statement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'while'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after condition.")
        body = self.statement()
        return Stmt.While(condition, body)
    
    def for_statement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'for'.")
        initializer = None
        if (self.match(TokenType.SEMICOLON)):
            pass
        elif (self.match(TokenType.VAR)):
            initializer = self.var_declaration()
        else:
            initializer = self.expression_statement()
        condition = None
        if (not self.check(TokenType.SEMICOLON)):
            condition = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after loop condition.")
        increment = None
        if (not self.check(TokenType.RIGHT_PAREN)):
            increment = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after for clauses.")
        body = self.statement()
        if (increment is not None):
            body = Stmt.Block([body, Stmt.Expression(increment)])
        if (condition is None):
            condition = Expr.Literal(True)
        body = Stmt.While(condition, body)
        if (initializer is not None):
            body = Stmt.Block([initializer, body])
        return body     
    
    def expression_statement(self):
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return Stmt.Expression(expr)
    
    def function(self, kind):
        name = self.consume(TokenType.IDENTIFIER, "Expect " + kind + " name.")
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after " + kind + " name.")
        parameters = []
        if (not self.check(TokenType.RIGHT_PAREN)):
            while True:
                if (len(parameters) >= 255):
                    raise ValueError("Can't have more than 255 parameters.")
                parameters.append(self.consume(TokenType.IDENTIFIER, "Expect parameter name."))
                if (not self.match(TokenType.COMMA)):
                    break
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after parameters.")
        self.consume(TokenType.LEFT_BRACE, "Expect '{' before " + kind + " body.")
        body = self.block()
        return Stmt.Function(name, parameters, body)
    
    def block(self):
        stmts = []
        while (not self.check(TokenType.RIGHT_BRACE) and not self.is_at_end()):
            stmts.append(self.declaration())
        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return stmts

    def assignment(self):
        expr = self.logic_or()
        if (self.match(TokenType.EQUAL)):
            equals = self.previous()
            value = self.assignment()
            if (isinstance(expr, Expr.Variable)):
                return Expr.Assign(expr.name, value)
            elif (isinstance(expr, Expr.Get)):
                return Expr.Set(expr.object, expr.name, value)
            raise ParseError("Invalid assignment target.")
        return expr
    
    
    def logic_or(self):
        expr = self.logic_and()
        while (self.match(TokenType.OR)):
            operator = self.previous()
            right = self.logic_and()
            expr = Expr.Logical(expr, operator, right)
        return expr
    
    def logic_and(self):
        expr = self.equality()
        while (self.match(TokenType.AND)):
            operator = self.previous()
            right = self.equality()
            expr = Expr.Logical(expr, operator, right)
        return expr

