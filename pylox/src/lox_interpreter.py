import Expr
import Stmt
from token_type import TokenType

class Interpreter(Expr.ExprVisitor, Stmt.StmtVisitor):
    def visit_literal_expr(self, expr):
        return expr.value
    
    def visit_grouping_expr(self, expr):
        return self.evaluate(expr.expr)
    
    def visit_unary_expr(self, expr):
        right = self.evaluate(expr.right)

        if (expr.operator.type == TokenType.MINUS):
            self.check_num_operand(right)
            return -1 * float(right)
        elif (expr.operator.type == TokenType.BANG):
            return not self.is_truthy(right)

        return None
    
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
        elif (expr.operator.type == TokenType.EQUAL):
            self.check_num_operands(left, right)
            return not self.is_equal(left, right)
        elif (expr.operator.type == TokenType.BANG_EQUAL):
            self.check_num_operands(left, right)
            return self.is_equal(left, right)
        elif (expr.operator.type == TokenType.PLUS):
            if (isinstance(left, float) and isinstance(right, float)):
                return float(left) + float(right)
            if (isinstance(left, str) and isinstance(right, str)):
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
    
    def check_num_operand(self, operand):
        if (isinstance(operand, float)):
            return
        raise RuntimeError("Operand must be a number.")
    
    def check_num_operands(self, left, right):
        if (isinstance(left, float) and isinstance(right, float)):
            return
        raise RuntimeError("Operands must be numbers.")

    def is_equal(self, a, b):
        if (a == None and b == None):
            return True
        elif (a == None):
            return False
        return a is b

    def evaluate(self, expr):
        return expr.accept(self)
    
    def visit_expression_stmt(self, stmt):
        self.evaluate(stmt.expr)
        return None
    
    def visit_print_stmt(self, stmt):
        value = self.evaluate(stmt.expr)
        print(self.stringify(value))
        return None
    
    def is_truthy(self, object):
        if (object == None):
            return False
        try:
            return bool(object)
        except:
            return True
        
    def interpret(self, statements):
        try:
            for statement in statements:
                self.execute(statement)
        except RuntimeError as error:
            raise error
        
    def execute(self, stmt):
        stmt.accept(self)
        
    def stringify(self, object):
        if (object == None):
            return "nil"
        if (isinstance(object, float)):
            text = str(object)
            if (text.endswith(".0")):
                text = text[0: len(text) - 2]

            return text
        
        return str(object)
