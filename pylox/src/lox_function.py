from lox_callable import LoxCallable
from environment import Environment
from lox_return import LoxReturn

class LoxFunction(LoxCallable):
    def __init__(self, declaration, closure, is_initializer):
        self.declaration = declaration
        self.closure = closure
        self.is_initializer = is_initializer

    def call(self, interpreter, arguments):
        environment = Environment(self.closure)
        for i in range(len(self.declaration.params)):
            environment.define(self.declaration.params[i].lexeme, arguments[i])
        try:
            interpreter.execute_block(self.declaration.body, environment)
        except LoxReturn as return_value:
            if (self.is_initializer):
                return self.closure.get_at(0, "this")
            return return_value.value
        if (self.is_initializer):
            return self.closure.get_at(0, "this")
        return None
    
    def arity(self):
        return len(self.declaration.params)
    
    def bind(self, instance):
        environment = Environment(self.closure)
        environment.define("this", instance)
        return LoxFunction(self.declaration, environment, self.is_initializer)

    def __str__(self):
        return "<fn " + self.declaration.lexeme + ">"
    
    
