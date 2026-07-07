import logger as log
from tok import TokenType

class Parser:
    def __init__(self, lexer, state, eval):
        self.lexer = lexer
        self.state = state
        self.eval = eval

        self.cur_token = None
        self.next_token()

    def check_type(self, type):
        return self.cur_token.type == type

    def match_type(self, type):
        if self.cur_token.type == type:
            self.next_token()
        else:
            log.error(f"invalid token ({self.cur_token.text})", self.cur_token.line)

    def next_token(self):
        self.cur_token = self.lexer.get_token()

    def skip_nl(self):
        while self.cur_token.type == TokenType.NL:
            self.next_token()

    def program(self):
        self.skip_nl()

        while self.cur_token.type != TokenType.EOF:
            self.statement()

    def statement(self):
        if self.check_type(TokenType.NOP):
            self.eval.add_instruction(self.cur_token.text, self.cur_token.line)
            self.eval.instruction_done()
            self.next_token()
        elif self.check_type(TokenType.MOV):
            self.eval.add_instruction(self.cur_token.text, self.cur_token.line)
            self.next_token()
            self.expression()
            self.eval.argument_done("src")
            self.match_type(TokenType.COMMA)
            self.dst()
            self.eval.argument_done("dst")
            self.eval.instruction_done()
        elif self.check_type(TokenType.SWP):
            self.eval.add_instruction(self.cur_token.text, self.cur_token.line)
            self.eval.instruction_done()
            self.next_token()
        elif self.check_type(TokenType.SAV):
            self.eval.add_instruction(self.cur_token.text, self.cur_token.line)
            self.eval.instruction_done()
            self.next_token()
        elif self.check_type(TokenType.ADD):
            self.eval.add_instruction(self.cur_token.text, self.cur_token.line)
            self.next_token()
            self.expression()
            self.eval.argument_done("src")
            self.eval.instruction_done()
        elif self.check_type(TokenType.SUB):
            self.eval.add_instruction(self.cur_token.text, self.cur_token.line)
            self.next_token()
            self.expression()
            self.eval.argument_done("src")
            self.eval.instruction_done()
        elif self.check_type(TokenType.NEG):
            self.eval.add_instruction(self.cur_token.text, self.cur_token.line)
            self.eval.instruction_done()
            self.next_token()
        elif self.check_type(TokenType.JMP):
            self.eval.add_instruction(self.cur_token.text, self.cur_token.line)
            self.next_token()
            self.eval.add_argument(self.cur_token)
            self.match_type(TokenType.IDENT)
            self.eval.argument_done("label")
            self.eval.instruction_done()
        elif self.check_type(TokenType.JEZ):
            self.eval.add_instruction(self.cur_token.text, self.cur_token.line)
            self.next_token()
            self.eval.add_argument(self.cur_token)
            self.match_type(TokenType.IDENT)
            self.eval.argument_done("label")
            self.eval.instruction_done()
        elif self.check_type(TokenType.JNZ):
            self.eval.add_instruction(self.cur_token.text, self.cur_token.line)
            self.next_token()
            self.eval.add_argument(self.cur_token)
            self.match_type(TokenType.IDENT)
            self.eval.argument_done("label")
            self.eval.instruction_done()
        elif self.check_type(TokenType.JGZ):
            self.eval.add_instruction(self.cur_token.text, self.cur_token.line)
            self.next_token()
            self.eval.add_argument(self.cur_token)
            self.match_type(TokenType.IDENT)
            self.eval.argument_done("label")
            self.eval.instruction_done()
        elif self.check_type(TokenType.JLZ):
            self.eval.add_instruction(self.cur_token.text, self.cur_token.line)
            self.next_token()
            self.eval.add_argument(self.cur_token)
            self.match_type(TokenType.IDENT)
            self.eval.argument_done("label")
            self.eval.instruction_done()
        elif self.check_type(TokenType.JRO):
            self.eval.add_instruction(self.cur_token.text, self.cur_token.line)
            self.next_token()
            self.expression()
            self.eval.argument_done("src")
            self.eval.instruction_done()
        # | ident ":"
        elif self.check_type(TokenType.IDENT):
            self.eval.add_label(self.cur_token.text, self.cur_token.line)
            self.next_token()
            self.match_type(TokenType.COLON)
            if self.check_type(TokenType.NL):
                self.nl()
            return
        elif self.check_type(TokenType.PUSH):
            self.eval.add_instruction(self.cur_token.text, self.cur_token.line)
            self.next_token()
            self.expression()
            self.eval.argument_done("src")
            self.eval.instruction_done()
        elif self.check_type(TokenType.POP):
            self.eval.add_instruction(self.cur_token.text, self.cur_token.line)
            self.next_token()
            self.dst()
            self.eval.argument_done("dst")
            self.eval.instruction_done()
        elif self.check_type(TokenType.READ):
            self.eval.add_instruction(self.cur_token.text, self.cur_token.line)
            self.next_token()
            self.eval.instruction_done()
        elif self.check_type(TokenType.WRITE):
            self.eval.add_instruction(self.cur_token.text, self.cur_token.line)
            self.next_token()
            self.expression()
            self.eval.argument_done("src")
            self.eval.instruction_done()
        elif self.check_type(TokenType.DEFINE):
            line = self.cur_token.line
            self.next_token()
            name = self.cur_token.text
            self.match_type(TokenType.IDENT)
            self.match_type(TokenType.COMMA)
            value = self.cur_token.text
            self.match_type(TokenType.NUMBER)
            self.eval.add_const(name, value, line)
        elif self.check_type(TokenType.CALL):
            self.eval.add_instruction(self.cur_token.text, self.cur_token.line)
            self.next_token()
            self.eval.add_argument(self.cur_token)
            self.match_type(TokenType.IDENT)
            self.eval.argument_done("label")
            self.eval.instruction_done()
        elif self.check_type(TokenType.RET):
            self.eval.add_instruction(self.cur_token.text, self.cur_token.line)
            self.next_token()
            self.eval.instruction_done()
        elif self.check_type(TokenType.DRAW):
            self.eval.add_instruction(self.cur_token.text, self.cur_token.line)
            self.next_token()
            self.eval.instruction_done()
        else:
            log.error(f"invalid token ({self.cur_token.text})", self.cur_token.line)

        self.nl()


    def dst(self):
        if self.check_type(TokenType.ACC):
            self.eval.add_argument(self.cur_token)
            self.next_token()
        elif self.check_type(TokenType.NIL):
            self.eval.add_argument(self.cur_token)
            self.next_token()
        # bp "(" expression ")"
        elif self.check_type(TokenType.BP):
            self.eval.add_argument(self.cur_token)
            self.next_token()
            if self.check_type(TokenType.OPEN_PAREN):
                self.eval.argument_append(self.cur_token)
                self.next_token()
                self.eval.argument_append(self.cur_token)
                self.match_type(TokenType.NUMBER)
                self.eval.argument_append(self.cur_token)
                self.match_type(TokenType.CLOSE_PAREN)
        elif self.check_type(TokenType.SP):
            self.eval.add_argument(self.cur_token)
            self.next_token()
            if self.check_type(TokenType.OPEN_PAREN):
                self.eval.argument_append(self.cur_token)
                self.next_token()
                self.eval.argument_append(self.cur_token)
                self.match_type(TokenType.NUMBER)
                self.eval.argument_append(self.cur_token)
                self.match_type(TokenType.CLOSE_PAREN)
        elif self.check_type(TokenType.ASTERISK):
            self.eval.add_argument(self.cur_token)
            self.next_token()
            if self.check_type(TokenType.BP):
                self.eval.argument_append(self.cur_token)
                self.next_token()
                self.eval.argument_append(self.cur_token)
                self.match_type(TokenType.OPEN_PAREN)
                self.eval.argument_append(self.cur_token)
                self.match_type(TokenType.NUMBER)
                self.eval.argument_append(self.cur_token)
                self.match_type(TokenType.CLOSE_PAREN)
            elif self.check_type(TokenType.SP):
                self.eval.argument_append(self.cur_token)
                self.next_token()
                self.eval.argument_append(self.cur_token)
                self.match_type(TokenType.OPEN_PAREN)
                self.eval.argument_append(self.cur_token)
                self.match_type(TokenType.NUMBER)
                self.eval.argument_append(self.cur_token)
                self.match_type(TokenType.CLOSE_PAREN)
            else:
                log.error(f"invalid token ({self.cur_token.text})", self.cur_token.line)
        else:
            log.error(f"invalid token ({self.cur_token.text})", self.cur_token.line)

    def expression(self):
        # | bp
        # | bp "(" primary ")"
        if self.check_type(TokenType.BP):
            self.eval.add_argument(self.cur_token)
            self.next_token()
            if self.check_type(TokenType.OPEN_PAREN):
                self.eval.argument_append(self.cur_token)
                self.next_token()
                self.eval.argument_append(self.cur_token)
                self.match_type(TokenType.NUMBER)
                self.eval.argument_append(self.cur_token)
                self.match_type(TokenType.CLOSE_PAREN)
        # | sp
        # | sp "(" primary ")"
        elif self.check_type(TokenType.SP):
            self.eval.add_argument(self.cur_token)
            self.next_token()
            if self.check_type(TokenType.OPEN_PAREN):
                self.eval.argument_append(self.cur_token)
                self.next_token()
                self.eval.argument_append(self.cur_token)
                self.match_type(TokenType.NUMBER)
                self.eval.argument_append(self.cur_token)
                self.match_type(TokenType.CLOSE_PAREN)
        # | "*" bp "(" primary ")"
        # | "*" sp "(" primary ")"
        elif self.check_type(TokenType.ASTERISK):
            self.eval.add_argument(self.cur_token)
            self.next_token()
            # "*" bp "(" primary ")"
            if self.check_type(TokenType.BP):
                self.eval.argument_append(self.cur_token)
                self.next_token()
                self.eval.argument_append(self.cur_token)
                self.match_type(TokenType.OPEN_PAREN)
                self.eval.argument_append(self.cur_token)
                self.match_type(TokenType.NUMBER)
                self.eval.argument_append(self.cur_token)
                self.match_type(TokenType.CLOSE_PAREN)
            # "*" sp "(" primary ")"
            elif self.check_type(TokenType.SP):
                self.eval.argument_append(self.cur_token)
                self.next_token()
                self.eval.argument_append(self.cur_token)
                self.match_type(TokenType.OPEN_PAREN)
                self.eval.argument_append(self.cur_token)
                self.match_type(TokenType.NUMBER)
                self.eval.argument_append(self.cur_token)
                self.match_type(TokenType.CLOSE_PAREN)
            else:
                log.error(f"invalid token ({self.cur_token.text})", self.cur_token.line)
        else:
            self.eval.add_argument(self.cur_token)
            return self.primary()

    def primary(self):
        if self.check_type(TokenType.NUMBER):
            self.next_token()
        elif self.check_type(TokenType.NIL):
            self.next_token()
        elif self.check_type(TokenType.ACC):
            self.next_token()
        elif self.check_type(TokenType.IDENT):
            if not self.cur_token.text in self.state.consts:
                log.error(f"({self.cur_token.text}) used but not defined", self.cur_token.line)
            self.next_token()
        else:
            log.error(f"invalid token ({self.cur_token.text})", self.cur_token.line)

    def nl(self):
        self.match_type(TokenType.NL)

        while self.check_type(TokenType.NL):
            self.next_token()
