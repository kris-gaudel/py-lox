import sys

TAB = '    '

class GenerateAst:
    def __init__(self):
        # self.args = sys.argv
        # self.outputDir = None # TODO: Add directory handling
        self.types = {
            "Binary": ('left', 'operator', 'right'),
            "Grouping": ('expr'),
            "Literal": ('value'),
            "Unary": ('operator', 'right')
            }
    
    def main(self):
        # TODO: Add directory handling
        # if (len(self.args) != 1):
        #     raise ValueError("Usage: generate_ast <output directory>")
        # self.outputDir = self.args[1]
        self.define_ast("Expr", self.types)
    
    def define_ast(self, baseName, types):
        path = baseName + ".py"
        file = open(path, "w")
        file.write('from abc import abstractmethod\n')
        file.write(f'class {baseName}:\n')
        file.write(f'{TAB}')
        file.write(f'@abstractmethod\n')
        file.write(f'{TAB}def __init__(self):\n')
        file.write(f'{TAB * 2}')
        file.write('pass\n')
        for className, fields in types.items():
            file.write('\n')
            self.define_type(file, baseName, className, fields)
    
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

# Sanity check
# g = GenerateAst()
# g.main()

        
