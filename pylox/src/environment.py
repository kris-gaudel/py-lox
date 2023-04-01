class Environment:
    def __init__(self, environment=None):
        self.values = {}
        self.enclosing = environment
    
    def define(self, name, object):
        self.values[name] = object

    def get(self, name):
        if name.lexeme in self.values.keys():
            return self.values[name.lexeme]
        if (self.enclosing is not None):
            return self.enclosing.get(name)
        raise RuntimeError("Undefined variable " + name.lexeme + ".")
    
    def assign(self, name, value):
        if (name.lexeme in self.values.keys()):
            self.values.update({name.lexeme: value})
            return None
        if (self.enclosing is not None):
            self.enclosing.assign(name, value)
            return None
        raise RuntimeError("Undefined variable '" + name.lexeme + "'.")
    
    