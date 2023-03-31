from abc import ABC, abstractmethod

class StmtVisitor(ABC):
    @abstractmethod
    def visit_expression_stmt(self, expr):
        pass

    @abstractmethod
    def visit_print_stmt(self, expr):
        pass

class Stmt:
    @abstractmethod
    def __init__(self):
        pass

class Expression(Stmt):
    def __init__(self, expr):
        self.expr = expr

    def accept(self, visitor):
        return visitor.visit_expression_stmt(self)

class Print(Stmt):
    def __init__(self, expr):
        self.expr = expr

    def accept(self, visitor):
        return visitor.visit_print_stmt(self)

