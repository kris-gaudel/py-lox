import sys
from scanner import Scanner
from lox_parser import Parser
from lox_interpreter import Interpreter
from token_type import TokenType
from lox_resolver import Resolver


class Lox:
    def __init__(self):
        self.args = sys.argv
        # self.has_error = False
        # self.has_runtime_error = False
        self.interpreter = Interpreter()
    
    def main(self):
        if (len(self.args) > 2):
            print("Usage: py-lox [script]")
        elif (len(self.args) == 2):
            self.run_file(self.args[1])
        else:
            self.run_prompt()

    def run_file(self, path):
        f = open(path)
        self.run(f.read())
        # if (self.has_error):
        #     sys.exit(65)

    def run_prompt(self):
        while True:
            prompt = input("py-lox>")
            self.run(prompt)
            # self.has_error = False

    def run(self, source):
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        statements = parser.parse()
        resolver = Resolver(self.interpreter)
        resolver.resolve_stmts(statements)
        # if (self.has_error or self.has_runtime_error):
        #     return
        # print(AstPrinter().print_expr(expression))
        self.interpreter.interpret(statements)
     
    def parse_error(self, token, message):
        if token.type == TokenType.EOF:
            self.report(token.line, "at end", message)
        else:
            self.report(token.line, " at '" + token.lexeme + "'", message)

    def error(self, line, message):
        self.report(line, "", message)
        #self.has_error = True
    
    def runtime_error(self, error):
        #self.has_runtime_error = True
        raise error
    
    def report(self, line, where, message):
        raise RuntimeError("[line " + line + "] Error" + where + ": " + message)
        # self.has_error = True

s = Lox()
s.main()