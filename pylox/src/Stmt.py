from abc import ABC, abstractmethod

class StmtVisitor(ABC):
    @abstractmethod
    def visit_block_stmt(self, expr):
        pass

    @abstractmethod
    def visit_expression_stmt(self, expr):
        pass

    @abstractmethod
    def visit_print_stmt(self, expr):
        pass

    @abstractmethod
    def visit_var_stmt(self, expr):
        pass

class Stmt:
    @abstractmethod
    def __init__(self):
        pass

class Block(Stmt):
    def __init__(self, stmts):
        self.stmts = stmts

    def accept(self, visitor):
        return visitor.visit_block_stmt(self)

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

class Var(Stmt):
    def __init__(self, name, initalizer):
        self.name = name
        self.initalizer = initalizer

    def accept(self, visitor):
        return visitor.visit_var_stmt(self)

