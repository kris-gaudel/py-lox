import sys

class Lox:
    def __init__(self):
        self.args = sys.argv
        self.has_error = False
    
    def main(self):
        if (len(self.args) > 1):
            print("Usage: py-lox [script]")
        elif (len(self.args) == 1):
            self.run_file(self.args[0])
        else:
            self.run_prompt()

    def run_file(self, path):
        f = open(path)
        self.run(f.read())
        if (self.has_error):
            raise ValueError("An error has occured!")

    def run_prompt(self):
        while True:
            prompt = input("py-lox>")
            self.run(prompt)
            self.has_error = False

    def run(self, source):
        scanner = Scanner(source)
        tokens = scanner.scanTokens()
        for token in tokens:
            print(token)
     
    def error(self, line, message):
        self.report(line, "", message)
    
    def report(self, line, where, message):
        print("[line " + line + "] Error" + where + ": " + message)
        self.has_error = True



