from arrows import *
from constants import *
from errors import *
from lexer import *
from parser import *


def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error:
        return None, error

    parser = Parser(tokens)
    ast = parser.parse()

    return ast.node, ast.error
