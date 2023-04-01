class Environment:
    def __init__(self):
        self.values = {}
    
    def define(self, name, object):
        self.values[name] = object

    def get(self, name):
        if name.lexeme in self.values.keys():
            return self.values[name.lexeme]
        raise RuntimeError("Undefined variable " + name.lexeme + ".")
    
    def assign(self, name, value):
        if (name.lexeme in self.values.keys()):
            self.values.update({name.lexeme: value})
            return None
        raise RuntimeError("Undefined variable '" + name.lexeme + "'.")
    
    