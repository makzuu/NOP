import sys


class Ins:
    def __init__(self, name, ln, params):
        self.name = name
        self.ln = ln
        self.params = params
    
    def __str__(self):
        return f"{self.ln} {self.name}: {self.params}"

def main():
    program = preprocess()
    for ins in program:
        print(ins)

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

def mov():
    ...


def add():
    ...


if __name__ == "__main__":
    main()
