from lexer import *
import sys

class Parser:
    # def __init__(self, lexer, eval):
    def __init__(self, lexer, state):
        self.lexer = lexer
        self.state = state
        # self.eval = eval

        self.initialize()

    def initialize(self):
        self.cur_token = None
        self.next_token()

    def check_type(self, type):
        return self.cur_token.type == type

    def match_type(self, type):
        if self.cur_token.type == type:
            self.next_token()
        else:
            self.print_and_exit(f"invalid token ({self.cur_token.text})")

    def next_token(self):
        self.cur_token = self.lexer.get_token()

    def print_and_exit(self, msg):
        error_msg = (
                "ERROR:\n"
                f"\tLine {self.cur_token.line}: {msg}"
                )
        sys.exit(error_msg)

    def skip_nl(self):
        while self.cur_token.type == TokenType.NL:
            self.next_token()

    def preprocess(self):
        self.skip_nl()

        while self.cur_token.type != TokenType.EOF:
            if self.check_type(TokenType.IDENT):
                label = self.cur_token.text
                line = self.cur_token.line
                self.next_token()
                if self.check_type(TokenType.COLON):
                    self.next_token()
                    if label in self.state.labels:
                        self.print_and_exit(f"{label} already defined")
                    else:
                        self.state.labels[label] = line
            self.next_token()
        self.initialize()

    def program(self):
        print("PROGRAM")

        self.skip_nl()

        while self.cur_token.type != TokenType.EOF:
            self.statement()

    # TODO:
    # - revisar que las labels no se repitan
    # - revisar que las labels a las que se salte existan
    # - quizas implementar un NOP para dejar en lugar de los labels
    # despues de definirlos o algo asi. no se, tengo sueño
    def statement(self):
        print("STATEMENT")

        if self.check_type(TokenType.NOP):
            ...
        elif self.check_type(TokenType.MOV):
            self.next_token()
            expression_value = self.expression()
            self.match_type(TokenType.COMMA)
            dst_value = self.dst()
            print(f"> MOV {expression_value}, {dst_value}")
        elif self.check_type(TokenType.SWP):
            self.next_token()
        elif self.check_type(TokenType.SAV):
            self.next_token()
        elif self.check_type(TokenType.ADD):
            self.next_token()
            expression_value = self.expression()
        elif self.check_type(TokenType.SUB):
            self.next_token()
            expression_value = self.expression()
        elif self.check_type(TokenType.NEG):
            self.next_token()
        elif self.check_type(TokenType.JMP):
            ...
        elif self.check_type(TokenType.JEZ):
            ...
        elif self.check_type(TokenType.JNZ):
            ...
        elif self.check_type(TokenType.JGZ):
            ...
        elif self.check_type(TokenType.JLZ):
            ...
        elif self.check_type(TokenType.JRO):
            self.next_token()
            expression_value = self.expression()
        elif self.check_type(TokenType.IDENT):
            ...
        elif self.check_type(TokenType.PUSH):
            self.next_token()
            expression_value = self.expression()
            self.state.push(expression_value)
        elif self.check_type(TokenType.POP):
            ...
        elif self.check_type(TokenType.READ):
            self.next_token()
        elif self.check_type(TokenType.WRITE):
            self.next_token()
            expression_value = self.expression()
        elif self.check_type(TokenType.DEFINE):
            ...
        elif self.check_type(TokenType.CALL):
            ...
        elif self.check_type(TokenType.RET):
            self.next_token()
        else:
            self.print_and_exit(f"invalid token ({self.cur_token.text})")

        self.nl()


    # TODO: hacer lo mismo que con expression
    def dst(self):
        print("DST")
        if self.check_type(TokenType.ACC):
            self.next_token()
            return "ACC"
        # bp "(" expression ")"
        elif self.check_type(TokenType.BP):
            self.next_token()
            if self.check_type(TokenType.OPEN_PAREN):
                self.next_token()
                primary_value = self.primary()
                self.match_type(TokenType.CLOSE_PAREN)
                # stack index
                return self.state.bp + primary_value
            return "BP"
        elif self.check_type(TokenType.SP):
            self.next_token()
            if self.check_type(TokenType.OPEN_PAREN):
                self.next_token()
                primary_value = self.primary()
                self.match_type(TokenType.CLOSE_PAREN)
                return self.state.sp + primary_value
            return "SP"
        elif self.check_type(TokenType.ASTERISK):
            self.next_token()
            if self.check_type(TokenType.BP):
                self.next_token()
                self.match_type(TokenType.OPEN_PAREN)
                primary_value = self.primary()
                self.match_type(TokenType.CLOSE_PAREN)
                return self.state.stack[self.state.bp + primary_value]
            elif self.check_type(TokenType.SP):
                self.next_token()
                self.match_type(TokenType.OPEN_PAREN)
                primary_value = self.primary()
                self.match_type(TokenType.CLOSE_PAREN)
                return self.state.stack[self.state.sp + primary_value]
            else:
                self.print_and_exit(f"invalid token ({self.cur_token.text})")
        else:
            self.print_and_exit(f"invalid token ({self.cur_token.text})")

    def expression(self):
        print("EXPRESSION")
        # | bp
        # | bp "(" primary ")"
        if self.check_type(TokenType.BP):
            self.next_token()
            if self.check_type(TokenType.OPEN_PAREN):
                self.next_token()
                primary_value = self.primary()
                self.match_type(TokenType.CLOSE_PAREN)
                # stack[bp + offset]
                return self.state.index(self.state.bp + primary_value)
            return self.state.bp
        # | sp
        # | sp "(" primary ")"
        elif self.check_type(TokenType.SP):
            self.next_token()
            if self.check_type(TokenType.OPEN_PAREN):
                self.next_token()
                primary_value = self.primary()
                self.match_type(TokenType.CLOSE_PAREN)
                # stack[sp + offset]
                return self.state.index(self.state.sp + primary_value)
            return self.state.sp
        # | "*" bp "(" primary ")"
        # | "*" sp "(" primary ")"
        elif self.check_type(TokenType.ASTERISK):
            self.next_token()
            # "*" bp "(" primary ")"
            if self.check_type(TokenType.BP):
                self.next_token()
                self.match_type(TokenType.OPEN_PAREN)
                primary_value = self.primary()
                self.match_type(TokenType.CLOSE_PAREN)
                # stack[stack[bp + offset]]
                return self.state.index(self.state.index(self.state.bp + primary_value))
            # "*" sp "(" primary ")"
            elif self.check_type(TokenType.SP):
                self.next_token()
                self.match_type(TokenType.OPEN_PAREN)
                primary_value = self.primary()
                self.match_type(TokenType.CLOSE_PAREN)
                # stack[stack[sp + offset]]
                return self.state.index(self.state.index(self.state.sp + primary_value))
            else:
                self.print_and_exit(f"invalid token ({self.cur_token.text})")
        else:
            return self.primary()

    def primary(self):
        if self.check_type(TokenType.NUMBER):
            number_value = int(self.cur_token.text)
            self.next_token()
            return number_value
        elif self.check_type(TokenType.NIL):
            self.next_token()
            return 0
        elif self.check_type(TokenType.ACC):
            self.next_token()
            return self.state.acc
        elif self.check_type(TokenType.IDENT):
            const_value = self.state.consts[self.cur_token.text]
            self.next_token()
            return const_value
        else:
            self.print_and_exit(f"invalid token ({self.cur_token.text})")

    def nl(self):
        print("NL")
        self.match_type(TokenType.NL)

        while self.check_type(TokenType.NL):
            self.next_token()
