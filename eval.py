import sys

class Stack:
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        try:
            return self.stack.pop()
        except IndexError:
            return 0

    def peek(self):
        return self.stack[-1]

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
        i = 0
        while i < len(self.instructions):
            if self.instructions[i].name == "MOV":
                src, dst = self.instructions[i].params
                self.mov(src, dst)
            elif self.instructions[i].name == "SWP":
                self.swp()
            elif self.instructions[i].name == "SAV":
                self.sav()
            elif self.instructions[i].name == "ADD":
                src = self.instructions[i].params[0]
                self.add(src)
            elif self.instructions[i].name == "SUB":
                src = self.instructions[i].params[0]
                self.sub(src)
            elif self.instructions[i].name == "NEG":
                self.neg()
            elif self.instructions[i].name == "JMP":
                label = self.instructions[i].params[0]
                y = self.jmp(label)
                if y != None:
                    i = y
            elif self.instructions[i].name == "JEZ":
                label = self.instructions[i].params[0]
                y = self.jez(label)
                if y != None:
                    i = y
            elif self.instructions[i].name == "JNZ":
                label = self.instructions[i].params[0]
                y = self.jnz(label)
                if y != None:
                    i = y
            elif self.instructions[i].name == "JGZ":
                label = self.instructions[i].params[0]
                y = self.jgz(label)
                if y != None:
                    i = y
            elif self.instructions[i].name == "JLZ":
                label = self.instructions[i].params[0]
                y = self.jlz(label)
                if y != None:
                    i = y
            elif self.instructions[i].name == "JRO":
                label = self.instructions[i].params[0]
                y = self.jro(label, i)
                if y != None:
                    i = y
            elif self.instructions[i].name == "PRINT":
                value = self.instructions[i].params[0]
                self.print(value)
            elif self.instructions[i].name == "NOP":
                self.add(0)
            else:
                sys.exit(f"invalid instruction ({self.instructions[i].name})")

            i += 1

    def get_input(self):
        try:
            return int(input("> "))
        except ValueError:
            return 0

    def mov(self, src, dst):
        src_value = 0
        if src == "ACC":
            src_value = self.state.acc
        elif src == "IN":
            src_value = self.get_input()
        elif src == "STACK":
            src_value = self.state.stack.pop()
        else: # number
            src_value = int(src)

        if dst == "ACC":
            self.state.acc = src_value
        # TODO: esto los deberia sacar despues
        elif dst == "OUT":
            print(src_value)
        elif dst == "STACK":
            self.state.stack.push(src_value)
        # TODO: queda para despues :>
        elif dst == "SCREEN":
            ...

    def swp(self):
        tmp = self.state.acc
        self.state.acc = self.state.bak
        self.state.bak = tmp

    def sav(self):
        self.state.bak = self.state.acc

    def add(self, src):
        src_value = 0
        if src == "ACC":
            src_value = self.state.acc
        elif src == "IN":
            src_value = self.get_value()
        elif src == "STACK":
            src_value = self.state.stack.pop()
        else: # number
            src_value = int(src)

        self.state.acc += src_value

    def sub(self, src):
        src_value = 0
        if src == "ACC":
            src_value = self.state.acc
        elif src == "IN":
            src_value = self.get_value()
        elif src == "STACK":
            src_value = self.state.stack.pop()
        else: # number
            src_value = int(src)

        self.state.acc -= src_value

    def neg(self):
        self.state.acc = -self.state.acc

    def jmp(self, label):
        try:
            return self.labels[label]
        except KeyError:
            sys.exit(f"label ({label}) not defined")

    def jez(self, label):
        if self.state.acc == 0:
            try:
                return self.labels[label]
            except KeyError:
                sys.exit(f"label ({label}) not defined")

    def jnz(self, label):
        if self.state.acc != 0:
            try:
                return self.labels[label]
            except KeyError:
                sys.exit(f"label ({label}) not defined")

    def jgz(self, label):
        if self.state.acc > 0:
            try:
                return self.labels[label]
            except KeyError:
                sys.exit(f"label ({label}) not defined")

    def jlz(self, label):
        if self.state.acc < 0:
            try:
                return self.labels[label]
            except KeyError:
                sys.exit(f"label ({label}) not defined")

    def jro(self, src, cur_i):
        src_value = 0
        if src == "ACC":
            src_value = self.state.acc
        elif src == "IN":
            src_value = self.get_input()
        elif src == "STACK":
            src_value = self.state.stack.pop()
        else: # number
            src_value = int(src)
        return cur_i + src_value

    def print(self, src):
        if src == "ACC":
            print(self.state.acc)
        elif src == "IN":
            print(self.get_input())
        elif src == "STACK":
            print(self.state.stack.peek())
        else: # string
            print(src)
