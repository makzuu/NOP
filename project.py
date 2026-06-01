import sys
from lexer import *
from parser import *

EOI = "EOI"

class Ins:
    def __init__(self, name, ln, params):
        self.name = name
        self.ln = ln
        self.params = params
    
    def __str__(self):
        return f"{self.ln} {self.name}: {self.params}"

class Stack:
    def __init__(self):
        self._stack = []
        self._index = -1

    def push(self, value):
        self._stack.append(value)
        self._index += 1

    def pop(self):
        if self._index < 0:
            return 0
        self._index -= 1
        return self._stack.pop()

    def peak(self):
        if self._index < 0:
            return 0
        return self._stack[-1]

    def __str__(self):
        return f"{self._stack}"

class State:
    def __init__(self):
        self.acc = 0

class Input:
    def __init__(self):
        self._input = []
        self._p = 0
        self._len = 0

    def add(self, n):
        self._input.append(n)
        self._len += 1

    def get(self):
        if self._p >= self._len:
            return EOI
        value = self._input[self._p]
        self._p += 1
        return value

state = State()
stack = Stack()
input = None


TOKEN_KIND_INT = "INTEGER"
TOKEN_KIND_INS = "INSTRUCTION"
TOKEN_KIND_COMMA = "COMMA"
TOKEN_KIND_REGISTER = "REGISTER"

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


def preprocess():
    program = []
    with open("program.t") as f:
        ln = 0
        for ins in f:
            ln += 1
            ins = ins.strip()
            if ins.startswith("#") or ins == "":
                continue
            name, *params = ins.split(" ")
            for i in range(len(params)):
                params[i] = params[i].rstrip(",")

            if name == "MOV":
                if len(params) != 2:
                    sys.exit(f"L: {ln} MOV: 2 parameter(s) expected, {len(params)} found")

                program.append(Ins("MOV", ln, params))
            elif name == "ADD":
                if len(params) != 1:
                    sys.exit(f"L: {ln} MOV: 2 parameter(s) expected, {len(params)} found")
                program.append(Ins("ADD", ln, params))

            else:
                sys.exit(f"L: {ln} {name}: invalid instruction")

    return program


def populate_input(filename):
    global input
    input = Input()
    try:
        with open(filename) as f:
            for value in f:
                try:
                    input.add(int(value))
                except ValueError:
                    sys.exit("invalid input {value}")
    except FileNotFoundError:
        sys.exit(f"input file {filename} not found")

# mov src, dst
# src: (IN | ACC | N)
# dst: (ACC | OUT)

# mov IN, ACC
# mov ACC, OUT
# mov N, (OUT | ACC)
def mov(src, dst, ln):
    if src == "IN":
        if input == None:
            sys.exit(f"L: {ln}, no input file provided")
        if dst == "ACC":
            value = input.get()
            if value == EOI:
                sys.exit(f"L: {ln} EOI ERROR")
            state.acc = value
        else:
            sys.exit(f"L: {ln} MOV: invalid dst {dst}")
    elif src == "ACC":
        if dst == "OUT":
            print(state.acc)
        else:
            sys.exit(f"L: {ln} MOV: invalid dst {dst}")
    elif src.isdecimal():
        if dst == "ACC":
            state.acc = int(src)
        elif dst == "OUT":
            print(src)
        else:
            sys.exit(f"L: {ln} MOV: invalid dst {dst}")
    else:
        sys.exit(f"L: {ln} MOV: invalid src {src}")

# add src
# src: (ACC | N | IN)
def add(src, ln):
    if src == "ACC":
        state.acc += state.acc
    elif src == "IN":
        if input == None:
            sys.exit(f"L: {ln}, no input file provided")
        value = input.get()
        if value == EOI:
            sys.exit(f"L: {ln} EOI ERROR")
        state.acc += value
    elif src.isdecimal():
        state.acc += int(src)
    else:
        sys.exit(f"L: {ln} ADD: invalid src {src}")


if __name__ == "__main__":
    main()
