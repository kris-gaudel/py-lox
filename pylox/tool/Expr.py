from abc import abstractmethod
class Expr:
    @abstractmethod
    def __init__(self):
        pass

class Binary(Expr):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class Grouping(Expr):
    def __init__(self, expr):
        self.expr = expr

class Literal(Expr):
    def __init__(self, value):
        self.value = value

class Unary(Expr):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right
