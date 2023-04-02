class LoxReturn(Exception):
    def __init__(self, value):
        super().__init__(None)
        self.value = value