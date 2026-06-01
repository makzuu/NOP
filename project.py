import sys
from lexer import *
from parser import *


def main():
    program = ""
    if len(sys.argv) != 2:
        sys.exit(f"usage:\n\tpython {sys.argv[0]} <file>")
    else:
        try:
            with open(sys.argv[1]) as f:
                program = f.read()
        except FileNotFoundError:
            sys.exit(f"could not open file {sys.argv[1]}")

    lexer = Lexer(program)
    parser = Parser(lexer)
    parser.program()


if __name__ == "__main__":
    main()
