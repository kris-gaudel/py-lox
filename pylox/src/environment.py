class Environment:
    def __init__(self, environment=None):
        self.values = {}
        self.enclosing = environment
    
    def define(self, name, object):
        self.values[name] = object
    
    def ancestor(self, distance):
        environment = self
        for _ in range(distance):
            environment = environment.enclosing
        return environment

    def get_at(self, distance, name):
        return self.ancestor(distance).values.get(name)
    
    def assign_at(self, distance, name, value):
        self.ancestor(distance).values.update({name.lexeme: value})

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
    
    