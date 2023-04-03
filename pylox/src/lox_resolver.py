import enum
import Expr
import Stmt

class FunctionType(enum.Enum):
    NONE = enum.auto()
    FUNCTION = enum.auto()
    INITIALIZER = enum.auto()
    METHOD = enum.auto()

class ClassType(enum.Enum):
    NONE = enum.auto()
    CLASS = enum.auto()

class Resolver(Expr.ExprVisitor, Stmt.StmtVisitor):
    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.scopes = []
        self.current_function = FunctionType.NONE
        self.current_class = FunctionType.NONE

    def visit_block_stmt(self, stmt):
        self.begin_scope()
        self.resolve_stmts(stmt.stmts)
        self.end_scope()
        return None
    
    def visit_class_stmt(self, stmt):
        enclosing_class = self.current_class
        self.current_class = ClassType.CLASS
        self.declare(stmt.name)
        self.define(stmt.name)
        self.begin_scope()
        self.scopes[len(self.scopes) - 1].update({"this": True})
        for method in stmt.methods:
            declaration = FunctionType.METHOD
            if (method.name.lexeme == "init"):
                declaration = FunctionType.INITIALIZER
            self.resolve_function(method, declaration)
        self.end_scope()
        self.current_class = enclosing_class
        return None
        
    
    def visit_expression_stmt(self, stmt):
        self.resolve(stmt.expr)
        return None
    
    def visit_function_stmt(self, stmt):
        self.declare(stmt.name)
        self.define(stmt.name)
        self.resolve_function(stmt, FunctionType.FUNCTION)
        return None
    
    def visit_if_stmt(self, stmt):
        self.resolve(stmt.condition)
        self.resolve(stmt.then_branch)
        if (stmt.else_branch is not None):
            self.resolve(stmt.else_branch)
        return None
    
    def visit_print_stmt(self, stmt):
        self.resolve(stmt.expr)
        return None
    
    def visit_return_stmt(self, stmt):
        if (self.current_function is FunctionType.NONE):
            raise ValueError("Can't return from top-level code.")
        if (stmt.value is not None):
            if (self.current_function is FunctionType.INITIALIZER):
                raise ValueError("Can't return a value from an initializer.")
            self.resolve(stmt.value)
        return None

    def visit_var_stmt(self, stmt):
        self.declare(stmt.name)
        if (stmt.initializer is not None):
            self.resolve(stmt.initializer)
        self.define(stmt.name)
        return None
    
    def visit_while_stmt(self, stmt):
        self.resolve(stmt.condition)
        self.resolve(stmt.body)
        return None
    
    def visit_assign_expr(self, expr):
        self.resolve(expr.value)
        self.resolve_local(expr, expr.name)
        return None
    
    def visit_binary_expr(self, expr):
        self.resolve(expr.left)
        self.resolve(expr.right)
        return None
    
    def visit_call_expr(self, expr):
        self.resolve(expr.callee)
        for arg in expr.arguments:
            self.resolve(arg)
        return None
    
    def visit_get_expr(self, expr):
        self.resolve(expr.object)
        return None
    
    def visit_grouping_expr(self, expr):
        self.resolve(expr.expr)
        return None
    
    def visit_literal_expr(self, expr):
        return None
    
    def visit_logical_expr(self, expr):
        self.resolve(expr.left)
        self.resolve(expr.right)
        return None
    
    def visit_set_expr(self, expr):
        self.resolve(expr.value)
        self.resolve(expr.object)
        return None
    
    def visit_this_expr(self, expr):
        if (self.current_class is ClassType.NONE):
            raise ValueError("Can't use 'this' outside of a class.")
        self.resolve_local(expr, expr.keyword)
        return None

    def visit_unary_expr(self, expr):
        self.resolve(expr.right)
        return None

    def visit_variable_expr(self, expr):
        if len(self.scopes) != 0 and self.scopes[-1].get(expr.name.lexeme) is False:
            self.on_error(
                expr.name, "Cannot read local variable in its own initializer."
            )
        self.resolve_local(expr, expr.name)
        return None

    def resolve_stmts(self, stmts):
        for stmt in stmts:
            self.resolve(stmt)

    def resolve(self, obj):
        obj.accept(self)

    def resolve_function(self, function, type):
        enclosing_function = self.current_function
        self.current_function = type
        self.begin_scope()
        for param in function.params:
            self.declare(param)
            self.define(param)
        self.resolve_stmts(function.body)
        self.end_scope()
        self.current_function = enclosing_function
    
    def begin_scope(self):
        self.scopes.append({})

    def end_scope(self):
        self.scopes.pop()

    def declare(self, name):
        if (len(self.scopes) == 0):
            return
        scope = self.scopes[len(self.scopes) - 1]
        if (name.lexeme in scope.keys()):
            raise ValueError("Already a variable with this name in this scope.")
        scope.update({name.lexeme: False})
    
    def define(self, name):
        if len(self.scopes) == 0:
            return
        scope = self.scopes[-1]
        scope[name.lexeme] = True

    def resolve_local(self, expr, name):
        for idx, scope in enumerate(reversed(self.scopes)):
            if name.lexeme in scope:
                self.interpreter.resolve(expr, idx)
                return