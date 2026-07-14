import logger as log
from token import TokenType

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
        print("STATEMENT")
        if self.check_type(TokenType.NOP):
            self.next_token()
        elif self.check_type(TokenType.MOV):
            self.next_token()
            self.src()
            self.match_type(TokenType.COMMA)
            self.dst()
        elif self.check_type(TokenType.SWP):
            self.next_token()
        elif self.check_type(TokenType.SAV):
            self.next_token()
        elif self.check_type(TokenType.ADD):
            self.next_token()
            self.src()
        elif self.check_type(TokenType.SUB):
            self.next_token()
            self.src()
        elif self.check_type(TokenType.NEG):
            self.next_token()
        elif self.check_type(TokenType.JMP):
            self.next_token()
            self.match_type(TokenType.IDENT)
        elif self.check_type(TokenType.JEZ):
            self.next_token()
            self.match_type(TokenType.IDENT)
        elif self.check_type(TokenType.JNZ):
            self.next_token()
            self.match_type(TokenType.IDENT)
        elif self.check_type(TokenType.JGZ):
            self.next_token()
            self.match_type(TokenType.IDENT)
        elif self.check_type(TokenType.JLZ):
            self.next_token()
            self.match_type(TokenType.IDENT)
        elif self.check_type(TokenType.JRO):
            self.next_token()
            self.src()
        # | ident ":"
        elif self.check_type(TokenType.IDENT):
            self.next_token()
            self.match_type(TokenType.COLON)
            if self.check_type(TokenType.NL):
                self.nl()
            return
        elif self.check_type(TokenType.PUSH):
            self.next_token()
            self.src()
        elif self.check_type(TokenType.POP):
            self.next_token()
            self.dst()
        elif self.check_type(TokenType.READ):
            self.next_token()
        elif self.check_type(TokenType.WRITE):
            self.next_token()
            self.src()
        elif self.check_type(TokenType.DEFINE):
            self.next_token()
            self.match_type(TokenType.IDENT)
            self.match_type(TokenType.COMMA)
            self.match_type(TokenType.NUMBER)
        elif self.check_type(TokenType.CALL):
            self.next_token()
            self.match_type(TokenType.IDENT)
        elif self.check_type(TokenType.RET):
            self.next_token()
        elif self.check_type(TokenType.DRAW):
            self.next_token()
        else:
            log.error(f"invalid token ({self.cur_token.text})", self.cur_token.line)

        self.nl()

    def src(self):
        print("SRC")
        if self.check_type(TokenType.ACC):
            self.next_token()
        elif self.check_type(TokenType.NIL):
            self.next_token()
        elif self.check_type(TokenType.NUMBER):
            self.next_token()
        elif self.check_type(TokenType.IDENT):
            self.next_token()
        elif self.check_type(TokenType.BP):
            self.next_token()
            if self.check_type(TokenType.OPEN_BRACKET):
                self.next_token()
                self.src()
                self.match_type(TokenType.CLOSE_BRACKET)
        elif self.check_type(TokenType.SP):
            self.next_token()
            if self.check_type(TokenType.OPEN_BRACKET):
                self.next_token()
                self.src()
                self.match_type(TokenType.CLOSE_BRACKET)
        else:
            log.error(f"invalid token ({self.cur_token.text})", self.cur_token.line)

    def dst(self):
        print("DST")
        if self.check_type(TokenType.ACC):
            self.next_token()
        elif self.check_type(TokenType.NIL):
            self.next_token()
        elif self.check_type(TokenType.IDENT):
            self.next_token()
        elif self.check_type(TokenType.BP):
            self.next_token()
            if self.check_type(TokenType.OPEN_BRACKET):
                self.next_token()
                self.src()
                self.match_type(TokenType.CLOSE_BRACKET)
        elif self.check_type(TokenType.SP):
            self.next_token()
            if self.check_type(TokenType.OPEN_BRACKET):
                self.next_token()
                self.src()
                self.match_type(TokenType.CLOSE_BRACKET)
        else:
            log.error(f"invalid token ({self.cur_token.text})", self.cur_token.line)


    def nl(self):
        self.match_type(TokenType.NL)

        while self.check_type(TokenType.NL):
            self.next_token()
