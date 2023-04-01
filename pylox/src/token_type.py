from enum import Enum

class TokenType(Enum):
    # Single-character tokens.
    LEFT_PAREN = '(',
    RIGHT_PAREN = ')', 
    LEFT_BRACE = '{'
    RIGHT_BRACE = '}'
    COMMA = ','
    DOT = '.'
    MINUS = '-'
    PLUS = '+'
    COLON = ':'
    SEMICOLON = ';'
    SLASH = '/'
    STAR = '*'

    # One or two character tokens.
    BANG = '!'
    BANG_EQUAL = '!='
    EQUAL = '='
    EQUAL_EQUAL = '=='
    GREATER = '>'
    GREATER_EQUAL = '>='
    LESS = '<'
    LESS_EQUAL = '<='

    # Literals.
    IDENTIFIER = 'identifier'
    STRING = 'str'
    NUMBER = 'num'
    # Keywords.
    AND = 'and'
    CLASS = 'class'
    ELSE = 'else'
    FALSE = 'false' 
    TRUE = 'true'
    FUN = 'fun'
    FOR = 'for' 
    IF = 'if' 
    NIL = 'nil' 
    OR = 'or'
    PRINT = 'print' 
    RETURN = 'return' 
    SUPER = 'super' 
    THIS = 'this' 
    VAR = 'var' 
    WHILE = 'while'

    EOF = ''