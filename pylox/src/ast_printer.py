import Expr
import scanner
import lox_token


class AstPrinter:

    def main(self):
        expression = Expr.Binary(
            Expr.Unary(
                lox_token.LoxToken(scanner.TokenType.MINUS, "-", None, 1),
                Expr.Literal(123)),
                lox_token.LoxToken(scanner.TokenType.STAR, "*", None, 1),
                Expr.Grouping(Expr.Literal(45.67)))
        print(AstPrinter().print_expr(expression))

    def print_expr(self, expr: Expr):
        return expr.accept(self)
    
    def visit_binary_expr(self, expr: Expr):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping_expr(self, expr: Expr):
        return self.parenthesize("group", expr.expr)
    
    def visit_literal_expr(self, expr: Expr):
        return str(expr.value)

    def visit_unary_expr(self, expr: Expr):
        return self.parenthesize(expr.operator.lexeme, expr.right)
    
    def parenthesize(self, name, *exprs):
        out = "(" + name

        for expr in exprs:
            out += " "
            out += expr.accept(self)
        
        out += ")"
        return out
    
a = AstPrinter()
a.main()