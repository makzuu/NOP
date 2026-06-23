class State:
    def __init__(self):
        self.acc = 0
        self.bak = 0
        self.stack = []
        self.bp = 0
        self.sp = len(self.stack)

        self.consts = {}
        self.labels = {}

    def push(self, value):
        self.stack.append(value)
        self.sp += 1

    def pop(self):
        try:
            value = self.stack.pop()
            self.sp -= 1
            return value
        except IndexError:
            return 0

    def index(self, i):
        try:
            return self.stack[i]
        except IndexError:
            return 0
