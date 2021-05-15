import sys
import logging
from zeroloader import ZeroLoader


class Zero:

    def __init__(self, filename):
        self.program = ZeroLoader(filename)


def main(filename):
    print("ZeroScript v0.0.1")
    print("Running: " + filename)

    Zero(filename)


if __name__ == "__main__":
    try:
        main(sys.argv[1])
    except IndexError:
        logging.fatal("No input file provided")
