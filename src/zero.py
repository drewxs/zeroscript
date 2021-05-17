from arrows import *
from constants import *
from errors import *
from nodes import *
from lexer import Lexer
from _parser import Parser


def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error:
        return None, error

    parser = Parser(tokens)
    ast = parser.parse()

    return ast.node, ast.error
