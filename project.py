import sys
from lexer import *
from parser import *
from state import State

def main():
    if len(sys.argv) < 2:
        sys.exit(f"usage: {sys.argv[0]} <program>")
    source = get_source(sys.argv[1])
    lex = Lexer(source)
    state = State()
    parser = Parser(lex, state)
    parser.program()


def get_source(filename):
    try:
        with open(filename) as f:
            source = f.read()
    except FileNotFoundError:
        sys.exit(f"file {filename} does not exist")
    return source


if __name__ == "__main__":
    main()
