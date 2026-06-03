class Stack:
    def __init__(self):
        self.stack = []
        self.top = -1

    def push(self, value):
        self.stack.append(value)
        self.top += 1

    def pop(self):
        if self.top < 0:
            return 0
        else:
            value = self.stack[self.top]
            self.top -= 1
            return value

class State:
    def __init__(self):
        self.acc = 0
        self.bak = 0
        self.stack = Stack()

class Ins:
    def __init__(self, name):
        self.name = name
        self.params = []

class Eval:
    def __init__(self):
        self.cur_ins = 0
        self.instructions = []
        self.labels = {}
        self.state = State()

    def add_ins(self, name):
        self.instructions.append(Ins(name))

    def add_label(self, name):
        if name in self.labels:
            sys.exit(f"label {name} already declared")
        self.labels[name] = self.cur_ins
        self.add_ins("NOP")
        self.done()

    def add_param(self, param):
        self.instructions[self.cur_ins].params.append(param)

    def done(self):
        self.cur_ins += 1

    def run(self):
        for ins in self.instructions:
            print(ins.name, ins.params)

        print(self.labels)

    def mov(self, src, dst):
        ...

    def swp(self):
        ...

    def sav(self):
        ...

    def add(self, src):
        src_value = 0
        if src == "ACC":
            src_value = self.state.acc
        elif src == "IN":
            # TODO: arreglar esto
            src_value = int(input("> "))
        elif src == "STACK":
            src_value = self.state.stack.pop()
        else: # number
            src_value = int(src)

        self.state.acc += src_value

    def sub(self, dst):
        ...

    def neg(self):
        ...

    def jez(self, label):
        ...

    def jnz(self, label):
        ...

    def jgz(self, label):
        ...

    def jlz(self, label):
        ...

    def jro(self, src):
        ...

    def print(self, src):
        # acc, in, stack
