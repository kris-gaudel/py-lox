import Expr
import Stmt
from time import time
from token_type import TokenType
from environment import Environment
from lox_callable import LoxCallable
from lox_function import LoxFunction
from lox_return import LoxReturn

class Interpreter(Expr.ExprVisitor, Stmt.StmtVisitor):
    def __init__(self) -> None:
        self.globals = Environment()
        self.environment = self.globals

        class Clock(LoxCallable):
            def __init__(self) -> None:
                super().__init__()
                self.start_time = time()
            def arity(self):
                return 0
            def call(self, interpreter, arguments):
                return time() - self.start_time
            def to_string(self):
                return "<native fn>;"
        self.globals.define("clock", Clock())

    def visit_literal_expr(self, expr):
        return expr.value
    
    def visit_logical_expr(self, expr):
        left = self.evaluate(expr.left)
        if (expr.operator.type is TokenType.OR):
            if (self.is_truthy(left)):
                return left
        else:
            if (not self.is_truthy(left)):
                return left
        return self.evaluate(expr.right)
    
    def visit_grouping_expr(self, expr):
        return self.evaluate(expr.expr)
    
    def visit_unary_expr(self, expr):
        right = self.evaluate(expr.right)

        if (expr.operator.type == TokenType.MINUS):
            self.check_num_operand(right)
            return -float(right)
        elif (expr.operator.type == TokenType.BANG):
            return not self.is_truthy(right)
        return None
    
    def visit_variable_expr(self, expr):
        return self.environment.get(expr.name)
    
    def visit_binary_expr(self, expr): 
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
        if (expr.operator.type == TokenType.MINUS):
            self.check_num_operands(left, right)
            return float(left) - float(right)
        elif (expr.operator.type == TokenType.GREATER):
            self.check_num_operands(left, right)
            return float(left) > float(right)
        elif (expr.operator.type == TokenType.GREATER_EQUAL):
            self.check_num_operands(left, right)
            return float(left) >= float(right)
        elif (expr.operator.type == TokenType.LESS):
            self.check_num_operands(left, right)
            return float(left) < float(right)
        elif (expr.operator.type == TokenType.LESS_EQUAL):
            self.check_num_operands(left, right)
            return float(left) <= float(right)
        elif (expr.operator.type == TokenType.EQUAL_EQUAL):
            self.check_num_operands(left, right)
            return self.is_equal(left, right)
        elif (expr.operator.type == TokenType.BANG_EQUAL):
            self.check_num_operands(left, right)
            return not self.is_equal(left, right)
        elif (expr.operator.type == TokenType.PLUS):
            if (isinstance(left, float) and isinstance(right, float)):
                return float(left) + float(right)
            else:
                return str(left) + str(right)
        elif (expr.operator.type == TokenType.SLASH):
            self.check_num_operands(left, right)
            if (right == 0.0):
                raise RuntimeError("Division by 0 is not allowed.")
            return float(left) / float(right)
        elif (expr.operator.type == TokenType.STAR):
            self.check_num_operands(left, right)
            return float(left) * float(right)
        return None
    
    def visit_call_expr(self, expr):
        callee = self.evaluate(expr.callee)
        arguments = []
        for argument in expr.arguments:
            arguments.append(self.evaluate(argument))
        if (not isinstance(callee, LoxCallable)):
            raise RuntimeError("Can only call functions and classes.")
        function = callee
        if (len(arguments) != function.arity()):
            raise RuntimeError("Expected " + function.arity() + "arguments but got " + len(arguments) + ".")
        
        return function.call(self, arguments)
    
    def check_num_operand(self, operand):
        if (isinstance(operand, float)):
            return
        raise RuntimeError("Operand must be a number.")
    
    def check_num_operands(self, left, right):
        if (isinstance(left, float) and isinstance(right, float)):
            return
        raise RuntimeError("Operands must be numbers.")

    def is_equal(self, a, b):
        if (a is None and b is None):
            return True
        elif (a is None):
            return False
        return a == b

    def evaluate(self, expr):
        return expr.accept(self)
    
    def visit_expression_stmt(self, stmt):
        self.evaluate(stmt.expr)
        return None
    
    def visit_function_stmt(self, stmt):
        function = LoxFunction(stmt, self.environment)
        self.environment.define(stmt.name.lexeme, function)
        return None

    def visit_if_stmt(self, stmt):
        if (self.is_truthy(self.evaluate(stmt.condition))):
            self.execute(stmt.then_branch)
        elif (stmt.else_branch is not None):
            self.execute(stmt.else_branch)
        return None
    
    def visit_print_stmt(self, stmt):
        value = self.evaluate(stmt.expr)
        print(self.stringify(value))
        return None
    
    def visit_return_stmt(self, stmt):
        value = None
        if (stmt.value is not None):
            value = self.evaluate(stmt.value)
        raise LoxReturn(value)
    
    def visit_var_stmt(self, stmt):
        value = None
        if (stmt.initalizer is not None):
            value = self.evaluate(stmt.initalizer)
        self.environment.define(stmt.name.lexeme, value)
        return None
    
    def visit_while_stmt(self, stmt):
        while (self.is_truthy(self.evaluate(stmt.condition))):
            self.execute(stmt.body)
        return None
    
    def visit_assign_expr(self, expr):
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value

    def is_truthy(self, object):
        if (object is None):
            return False
        elif (isinstance(object, bool)):
            return bool(object)
        return True
        
    def interpret(self, statements):
        try:
            for statement in statements:
                self.execute(statement)
        except RuntimeError as error:
            raise error
        
    def execute(self, stmt):
        stmt.accept(self)

    def execute_block(self, stmts, environment):
        previous = self.environment
        try:
            self.environment = environment
            for stmt in stmts:
                self.execute(stmt)
        finally:
            self.environment = previous
    
    def visit_block_stmt(self, stmt):
        self.execute_block(stmt.stmts, Environment(self.environment))
        return None
        
    def stringify(self, object):
        if (object is None):
            return "nil"
        if (isinstance(object, float) or isinstance(object, str)):
            text = str(object)
            if (text.endswith(".0")):
                text = text[0: len(text) - 2]

            return text
        
        return str(object)
