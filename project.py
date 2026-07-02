import sys
from lexer import *
from parser import *
from state import State
from eval import *

def main():
    if len(sys.argv) < 2:
        sys.exit(f"usage: {sys.argv[0]} <program>")
    source = get_source(sys.argv[1])
    lex = Lexer(source)
    state = State()
    eval = Eval(state)
    parser = Parser(lex, state, eval)
    parser.program()
    eval.run()

    #debug(state)


def get_source(filename):
    try:
        with open(filename) as f:
            source = f.read()
    except FileNotFoundError:
        sys.exit(f"file {filename} does not exist")
    return source


def debug(state):
    print("<DEBUG")
    print(f"acc = {state.acc}, bak = {state.bak}, bp = {state.bp}, sp = {state.sp}")
    print(f"stack = {state.stack}")
    print("Labels:")
    for label in state.labels:
        print(f"\t{label}: {state.labels[label]}")
    print("Consts:")
    for const in state.consts:
        print(f"\t{const}: {state.consts[const]}")
    print("DEBUG>")


if __name__ == "__main__":
    main()
