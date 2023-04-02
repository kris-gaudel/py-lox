import sys

TAB = '    '

class GenerateAst:
    def __init__(self):
        # self.args = sys.argv
        # self.outputDir = None # TODO: Add directory handling
        self.expressions = {
            "Assign": ('name', 'value'),
            "Binary": ('left', 'operator', 'right'),
            "Grouping": ('expr'),
            "Literal": ('value'),
            "Logical": ('left', 'operator', 'right'),
            "Unary": ('operator', 'right'),
            "Variable": ('name')
            }
        self.statements = {
            "Block": ('stmts'),
            "Expression": ('expr'),
            "If": ('condition', 'then_branch', 'else_branch'),
            "Print": ('expr'),
            "Var": ('name', 'initalizer'),
            "While": ('condition', 'body')
        }
    
    def main(self):
        # TODO: Add directory handling
        # if (len(self.args) != 1):
        #     raise ValueError("Usage: generate_ast <output directory>")
        # self.outputDir = self.args[1]
        self.define_ast("Expr", self.expressions)
        self.define_ast("Stmt", self.statements)

    
    def define_ast(self, baseName, types):
        path = "../src/" + baseName + ".py"
        file = open(path, "w")
        file.write('from abc import ABC, abstractmethod\n')
        self.define_visitor(file, baseName, types)
        file.write(f'class {baseName}:\n')
        file.write(f'{TAB}')
        file.write(f'@abstractmethod\n')
        file.write(f'{TAB}def __init__(self):\n')
        file.write(f'{TAB * 2}')
        file.write('pass\n')
        for className, fields in types.items():
            file.write('\n')
            self.define_type(file, baseName, className, fields)
        file.write('\n')
    
    def define_type(self, file, baseName, className, fields):
        file.write(f'class {className}({baseName}):')
        file.write('\n')
        file.write(f'{TAB}')
        if type(fields) is not tuple:
            file.write(f'def __init__(self, {fields}):')
            file.write('\n')
        else:
            file.write(f'def __init__(self, {", ".join(fields)}):')
            file.write('\n')
        if type(fields) is not tuple:
            file.write(f'{TAB * 2}self.{fields} = {fields}')
            file.write('\n')
        else:
            for field in fields:
                att = field.split(":")[0]
                file.write(f'{TAB * 2}self.{att} = {att}')
                file.write('\n')
        file.write('\n')
        file.write(f'{TAB}def accept(self, visitor):\n')
        file.write(f'{TAB * 2}return visitor.visit_{className.lower()}_{baseName.lower()}(self)')
        file.write('\n')
        
    def define_visitor(self, file, baseName, types):
        visitor = f'{baseName}Visitor'
        file.write(f'\n')
        file.write(f'class {visitor}(ABC):')

        for type in types:
            file.write('\n')
            file.write(f'{TAB}@abstractmethod')
            file.write('\n')
            file.write(f'{TAB}')
            file.write(f"def visit_{type.lower()}_{baseName.lower()}(self, expr):")
            file.write('\n')
            file.write(f'{TAB * 2}pass')
            file.write('\n')
        file.write(f'\n')


#Sanity check
g = GenerateAst()
g.main()

        
