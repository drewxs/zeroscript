from Lexer import Lexer
from Parser import Parser
from Evaluator import Evaluator


def main():
    filename = 'hello.zero'
    file = open(filename, 'r')
    lexer = Lexer(file)
    parser = Parser(lexer.tokens)

    lexer.tokenizer()
    print("TOKENS:")
    print(lexer.tokens, "\n")

    parser.build_AST()
    print("AST:")
    print(parser.AST, "\n")

    evaluator = Evaluator(parser.AST)

    print("OUTPUT:")
    evaluator.run(parser.AST)


if __name__ == "__main__":
    main()
