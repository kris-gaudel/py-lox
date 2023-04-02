from lox_callable import LoxCallable
from environment import Environment
from lox_return import LoxReturn

class LoxFunction(LoxCallable):
    def __init__(self, declaration) -> None:
        self.declaration = declaration

    def call(self, interpreter, arguments):
        environment = Environment(interpreter.globals)
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
    
    
