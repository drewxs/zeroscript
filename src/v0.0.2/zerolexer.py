from enum import Enum


class LexState(Enum):
    INIT = 1
    COMMENT = 2
    DELIMITER = 3
    NUMERIC = 4
    OPERATOR = 5
    VARIABLE = 6
    KEYWORD = 7


class HandleState(Enum):
    READ = 1
    WRITE = 2


class ZeroLexer:

    def __init__(self):
        self.state = LexState.INIT
        self.hstate = HandleState.READ
        self.buffer = []
        self.tokens = []

    def Run(self, line):
        for char in line:
            # print(f"char: {char}")
            self.getState(char)
            self.handleState()

    def getState(self, char):
        self.state, self.hstate, self.buffer = ZeroState(
            self.state, self.hstate, self.buffer, char
        ).NextState()

    def handleState(self):
        token = ZeroState(
            self.state, self.hstate, "".join(self.buffer), None
        ).StateToken()

        if token:
            self.tokens.append(token)
            self.state = LexState.INIT
            self.hstate = HandleState.READ
            self.buffer = []


class ZeroState:

    def __init__(self, state, hstate, buf, char):
        self.state = state
        self.hstate = hstate
        self.buffer = buf
        self.char = char
        self.delimiters = [":", " ", "{", "}", "\n", "\t"]
        self.operators = ["+", "-", "*", "/", "="]
        self.keywords = ["to", "as"]

    def NextState(self):
        if self.state == LexState.INIT:
            return self.init_state()
        elif self.char == LexState.OPERATOR:
            return self.operator_state()
        elif self.char == LexState.COMMENT:
            return self.comment_state()
        elif self.char == LexState.VARIABLE:
            return self.variable_state()
        elif self.char == LexState.DELIMITER:
            return self.delimiter_state()
        elif self.char == LexState.NUMERIC:
            return self.numeric_state()

        return self.state, self.hstate, self.buffer

    def StateToken(self):
        if self.hstate == HandleState.WRITE:
            return {'id': self.state, 'value': self.buffer}

        return None

    def init_state(self):
        self.buffer.append(self.char)

        if self.char in self.operators:
            return LexState.OPERATOR, HandleState.READ, self.buffer
        if self.char in self.delimiters:
            return LexState.DELIMITER, HandleState.WRITE, self.buffer
        if self.iskeyword(self.buffer):
            return LexState.KEYWORD, HandleState.WRITE, self.buffer
        if self.isnumeric(self.buffer):
            return LexState.NUMERIC, HandleState.READ, self.buffer
        else:
            return LexState.VARIABLE, HandleState.READ, self.buffer

    def operator_state(self):
        if self.char in self.delimiters:
            return LexState.OPERATOR, HandleState.WRITE, self.buffer

        self.buffer.append(self.char)
        return LexState.COMMENT, HandleState.READ, []

    def comment_state(self):
        if self.char == "\n":
            return LexState.COMMENT, HandleState.WRITE, self.buffer

        self.buffer.append(self.char)
        return LexState.COMMENT, HandleState.READ, self.buffer

    def variable_state(self):
        if self.char in self.delimiters:
            if self.iskeyword(self.buffer):
                return LexState.KEYWORD, HandleState.WRITE, self.buffer
            else:
                return LexState.VARIABLE, HandleState.WRITE, self.buffer
        else:
            self.buffer.append(self.char)
            return self.state, self.hstate, self.buffer

    def delimiter_state(self):
        return LexState.DELIMITER, HandleState.WRITE, self.buffer

    def numeric_state(self):
        if self.char in self.delimiters:
            return LexState.NUMERIC, HandleState.WRITE, self.buffer
        else:
            self.buffer.append(self.char)
            return LexState.NUMERIC, HandleState.READ, self.buffer

    def iskeyword(self, b):
        return "".join(b) in self.keywords

    def isnumeric(self, b):
        try:
            int("".join(b))
            return True
        except ValueError:
            return False
