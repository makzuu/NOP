import logger as log

class State:
    def __init__(self):
        self.acc = 0
        self.bak = 0
        self.stack = []
        self.bp = 0
        self.sp = 0

        self.line = None

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
            log.error(f"stack is empty", self.line)

    def index(self, i):
        try:
            return self.stack[i]
        except IndexError:
            log.error(f"index ({i}) out of bounds", self.line)

    def insert(self, i, value):
        try:
            if i < 0:
                log.error(f"index ({i}) out of bounds", self.line)
            self.stack[i] = value
        except IndexError:
            log.error(f"index ({i}) out of bounds", self.line)
