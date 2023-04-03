class LoxInstance:
    def __init__(self, klass):
        self.klass = klass
        self.fields = {}

    def __str__(self):
        return self.klass.name + " instance"
    
    def get(self, name):
        if (name.lexeme in self.fields.keys()):
            return self.fields.get(name.lexeme)
        method = self.klass.find_method(name.lexeme)
        if (method is not None):
            return method.bind(self)
        raise RuntimeError("Undefined property '" + name.lexeme +"'.")
    
    def set(self, name, value):
        self.fields.update({name.lexeme: value})
