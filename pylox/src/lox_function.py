from lox_callable import LoxCallable
from environment import Environment
from lox_return import LoxReturn

class LoxFunction(LoxCallable):
    def __init__(self, declaration, closure) -> None:
        self.declaration = declaration
        self.closure = closure

    def call(self, interpreter, arguments):
        environment = Environment(self.closure)
        for i in range(len(self.declaration.params)):
            environment.define(self.declaration.params[i].lexeme, arguments[i])
        try:
            interpreter.execute_block(self.declaration.body, environment)
        except LoxReturn as return_value:
            return return_value.value
        return None
    
    def arity(self):
        return len(self.declaration.params)
    
    def to_string(self):
        return "<fn " + self.declaration.lexeme + ">"
    
    
