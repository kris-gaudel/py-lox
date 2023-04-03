from lox_callable import LoxCallable
from lox_instance import LoxInstance

class LoxClass(LoxCallable):
    def __init__(self, name, methods):
        self.name = name
        self.methods = methods

    def __str__(self):
        return self.name
    
    def find_method(self, name):
        if (name in self.methods.keys()):
            return self.methods.get(name)
        return None

    def call(self, interpreter, args):
        instance = LoxInstance(self)
        initializer = self.find_method("init")
        if (initializer is not None):
            initializer.bind(instance).call(interpreter, args)
        return instance

    def arity(self):
        initializer = self.find_method("init")
        if (initializer is None):
            return 0
        return initializer.arity()