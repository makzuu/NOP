import sys
import logger as log
from tok import TokenType
from img import Img

class Instruction:
    def __init__(self, name, params, line):
        self.name = name
        self.params = params
        self.line = line

class Eval:
    def __init__(self, state):
        self.instructions = []
        self.tmp_instruction = None
        self.tmp_argument = None

        self.state = state
        self.img = None

    def add_label(self, name, line):
        if name in self.state.labels:
            log.error(f"label {name} already exists", line)
        self.state.labels[name] = len(self.instructions)

    def add_const(self, name, value, line):
        if name in self.state.consts:
            log.warning("{name} already defined", line)
            return
        self.state.consts[name] = self.limit(int(value))

    def add_instruction(self, name, line):
        self.tmp_instruction = Instruction(name, {}, line)

    def add_argument(self, argument):
        self.tmp_argument = []
        self.tmp_argument.append(argument)

    def argument_append(self, part):
        self.tmp_argument.append(part)

    def argument_done(self, name):
        self.tmp_instruction.params[name] = self.tmp_argument

    def instruction_done(self):
        self.instructions.append(self.tmp_instruction)

    def get_src_value(self, src_tokens):
        if src_tokens[0].type == TokenType.BP:
            offset = 0
            if len(src_tokens) > 1:
                offset = int(src_tokens[2].text)
                return self.state.index(self.state.bp + offset)
            return self.state.bp
        elif src_tokens[0].type == TokenType.SP:
            offset = 0
            if len(src_tokens) > 1:
                offset = int(src_tokens[2].text)
                return self.state.index(self.state.sp + offset)
            return self.state.sp
        elif src_tokens[0].type == TokenType.ASTERISK:
            return self.state.index(self.get_src_value(src_tokens[1:]))
        else:
            return self.get_primary_value(src_tokens[0])

    def get_dst_index(self, dst_tokens):
        if dst_tokens[0].type == TokenType.BP:
            return self.state.bp + int(dst_tokens[2].text)
        elif dst_tokens[0].type == TokenType.SP:
            return self.state.sp + int(dst_tokens[2].text)
        elif dst_tokens[0].type == TokenType.ASTERISK:
            return self.get_src_value(dst_tokens[1:])

    def get_primary_value(self, token):
        if token.type == TokenType.ACC:
            return self.state.acc
        elif token.type == TokenType.NIL:
            return 0
        elif token.type == TokenType.NUMBER:
            return self.limit(int(token.text))
        elif token.type == TokenType.IDENT:
            return self.state.consts[token.text]

    def limit(self, number, low=-999, high=999):
        if number > high:
            return high
        if number < low:
            return low
        return number

    def get_instruction_number(self, label, line):
        if label not in self.state.labels:
            log.error(f"Label ({label}) is not defined", line)
        return self.state.labels[label]


    def run(self):
        self.instructions.append(Instruction("NOP", None, None))

        # TODO
        i_num = 0
        while i_num < len(self.instructions):
            self.state.line = self.instructions[i_num].line

            i_name = self.instructions[i_num].name
            i_params = self.instructions[i_num].params
            i_line = self.instructions[i_num].line

            # mov src, dst
            if i_name == TokenType.MOV.name:
                src = self.get_src_value(i_params["src"])

                if i_params["dst"][0].type == TokenType.ACC:
                    self.state.acc = src
                elif i_params["dst"][0].type == TokenType.NIL:
                    NIL = src
                elif i_params["dst"][0].type == TokenType.BP and len(i_params["dst"]) == 1:
                    self.state.bp = self.limit(src, low=0)
                elif i_params["dst"][0].type == TokenType.SP and len(i_params["dst"]) == 1:
                    self.state.sp = self.limit(src, low=0)
                else:
                    dst = self.get_dst_index(i_params["dst"])
                    self.state.insert(dst, src)

            elif i_name == TokenType.SWP.name:
                tmp = self.state.acc
                self.state.acc = self.state.bak
                self.state.bak = tmp

            elif i_name == TokenType.SAV.name:
                self.state.bak = self.state.acc

            elif i_name == TokenType.ADD.name:
                src = self.get_src_value(i_params["src"])
                self.state.acc = self.limit(self.state.acc + src)

            elif i_name == TokenType.SUB.name:
                src = self.get_src_value(i_params["src"])
                self.state.acc = self.limit(self.state.acc - src)

            elif i_name == TokenType.NEG.name:
                self.state.acc *= -1

            elif i_name == TokenType.JMP.name:
                label = i_params["label"][0].text
                line = i_params["label"][0].line

                i_num = self.get_instruction_number(label, line)
                continue

            elif i_name == TokenType.JEZ.name:
                label = i_params["label"][0].text
                line = i_params["label"][0].line

                if self.state.acc == 0:
                    i_num = self.get_instruction_number(label, line)
                    continue

            elif i_name == TokenType.JNZ.name:
                label = i_params["label"][0].text
                line = i_params["label"][0].line

                if self.state.acc != 0:
                    i_num = self.get_instruction_number(label, line)
                    continue

            elif i_name == TokenType.JGZ.name:
                label = i_params["label"][0].text
                line = i_params["label"][0].line

                if self.state.acc > 0:
                    i_num = self.get_instruction_number(label, line)
                    continue

            elif i_name == TokenType.JLZ.name:
                label = i_params["label"][0].text
                line = i_params["label"][0].line

                if self.state.acc < 0:
                    i_num = self.get_instruction_number(label, line)
                    continue

            elif i_name == TokenType.JRO.name:
                i_num = self.limit(self.get_src_value(i_params["src"]), low=0, high=len(self.instructions) - 1)
                continue

            elif i_name == TokenType.PUSH.name:
                self.state.push(self.get_src_value(i_params["src"]))

            elif i_name == TokenType.POP.name:
                if i_params["dst"][0].type == TokenType.ACC:
                    self.state.acc = self.state.pop()
                elif i_params["dst"][0].type == TokenType.NIL:
                    NIL = self.state.pop()
                elif i_params["dst"][0].type == TokenType.BP and len(i_params["dst"]) == 1:
                    self.state.bp = self.limit(self.state.pop(), low=0)
                elif i_params["dst"][0].type == TokenType.SP and len(i_params["dst"]) == 1:
                    self.state.sp = self.limit(self.state.pop(), low=0)
                else:
                    self.state.insert(self.get_dst_index(i_params["dst"]), self.state.pop())

            elif i_name == TokenType.READ.name:
                if self.img == None:
                    try:
                        number = self.limit(int(input("< ")))
                    except ValueError:
                        number = 0
                else:
                    try:
                        number = self.limit(int(self.img.get_input()))
                    except ValueError:
                        number = 0
                self.state.push(number)

            elif i_name == TokenType.WRITE.name:
                if self.img == None:
                    print("> " + str(self.get_src_value(i_params["src"])))
                else:
                    self.img.write_output("> " + str(self.get_src_value(i_params["src"])))

            elif i_name == TokenType.CALL.name:
                self.state.push(i_num + 1)
                label = i_params["label"][0].text
                i_num = self.get_instruction_number(label, i_line)
                continue

            elif i_name == TokenType.RET.name:
                i_num = self.state.pop()
                continue

            elif i_name == TokenType.DRAW.name:
                if self.img == None:
                    self.img = Img()
                self.img.draw(self.state.stack[self.state.bp:self.state.sp])

            i_num += 1
