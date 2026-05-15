import sys


class Ins:
    def __init__(self, name, ln, params):
        self.name = name
        self.ln = ln
        self.params = params
    
    def __str__(self):
        return f"{self.ln} {self.name}: {self.params}"

# the stack also stores input
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

state = State()
stack = Stack()

def main():
    if len(sys.argv) == 2:
        populate_stack(sys.argv[1])
    program = preprocess()
    for ins in program:
        if ins.name == "MOV":
            mov(ins.params[0], ins.params[1], ins.ln)
        elif ins.name == "ADD":
            add(ins.params[0], ins.ln)


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


def populate_stack(filename):
    try:
        with open(filename) as f:
            for value in f:
                try:
                    stack.push(int(value))
                except ValueError:
                    sys.exit("invalid input {value}")
    except FileNotFoundError:
        sys.exit(f"input file {filename} not found")

def mov(src, dst, ln):
    if src == "IN":
        if dst == "ACC":
            state.acc += stack.pop()
        else:
            sys.exit(f"L: {ln} MOV: invalid dst {dst}")
    elif src == "ACC":
        if dst == "OUT":
            print(state.acc)
        else:
            sys.exit(f"L: {ln} MOV: invalid dst {dst}")
    else:
        sys.exit(f"L: {ln} MOV: invalid src {src}")


def add(src, ln):
    if src == "ACC":
        state.acc += state.acc
    else:
        sys.exit(f"L: {ln} ADD: invalid src {src}")


if __name__ == "__main__":
    main()
