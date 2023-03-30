import Expr
from token_type import TokenType
class Interpreter(Expr.ExprVisitor):
    def visit_literal_expr(self, expr):
        return expr.value
    
    def visit_grouping_expr(self, expr):
        return self.evaluate(expr.expression)
    
    def visit_unary_expr(self, expr):
        right = self.evaluate(expr.right)

        if (expr.operator.type == TokenType.MINUS):
            return -1 * float(right)
        elif (expr.operator.type == TokenType.BANG):
            return not self.is_truthy(right)

        return None
    
    #def visit_binary_expr(self, expr): 

    def evaluate(self, expr):
        return expr.accept(self)
    
    def is_truthy(self, object):
        if (object == None):
            return False
        try:
            return bool(object)
        except:
            return True


