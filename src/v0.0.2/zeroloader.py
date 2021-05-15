from zerolexer import ZeroLexer
from zeroparser import ZeroParser
from zeroeval import ZeroEval


class ZeroLoader:

    def __init__(self, filename):
        prog = Program(open(filename, "r"))
        prog.Run()


class Program:

    def __init__(self, fh):
        self.code = fh
        self.tokens = []

    def Run(self):
        for line in self.code:
            #print(f"line: {line}")

            lexer = ZeroLexer()
            lexer.Run(line)

            for token in lexer.tokens:
                self.tokens.append(token)

        parser = ZeroParser(self.tokens)
        parser.Run()

        evaluator = ZeroEval(parser.ast)
        evaluator.Run()

        print(f"tokens: {self.tokens}")
        print(f"ast: {parser.ast}")
        print(f"output: {evaluator.output}")
