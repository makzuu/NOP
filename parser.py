from lexer import *
import sys

class Parser:
    def __init__(self, lexer, eval):
        self.lexer = lexer
        self.eval = eval

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

    def program(self):
        print("PROGRAM")

        while self.cur_token.type == TokenType.NL:
            self.next_token()

        while self.cur_token.type != TokenType.EOF:
            self.statement()

    # TODO:
    # - revisar que las labels no se repitan
    # - revisar que las labels a las que se salte existan
    # - quizas implementar un NOP para dejar en lugar de los labels
    # despues de definirlos o algo asi. no se, tengo sueño
    def statement(self):
        print("STATEMENT")
        # ident ":"
        if self.check_type(TokenType.IDENT):
            self.eval.add_label(self.cur_token.text)
            self.next_token()
            self.match_type(TokenType.COLON)
        # "MOV" src "," dst
        elif self.check_type(TokenType.MOV):
            self.eval.add_ins("MOV")
            self.next_token()
            self.src()
            self.match_type(TokenType.COMMA)
            self.dst()
            self.eval.done()
        # "SWP"
        elif self.check_type(TokenType.SWP):
            self.eval.add_ins("SWP")
            self.eval.done()
            self.next_token()
        # "SAV"
        elif self.check_type(TokenType.SAV):
            self.eval.add_ins("SAV")
            self.eval.done()
            self.next_token()
        # "ADD" src
        elif self.check_type(TokenType.ADD):
            self.eval.add_ins("ADD")
            self.next_token()
            self.src()
            self.eval.done()
        # "SUB" src
        elif self.check_type(TokenType.SUB):
            self.eval.add_ins("SUB")
            self.next_token()
            self.src()
            self.eval.done()
        # "NEG"
        elif self.check_type(TokenType.NEG):
            self.eval.add_ins("NEG")
            self.eval.done()
            self.next_token()
        # "JMP" ident
        elif self.check_type(TokenType.JMP):
            self.eval.add_ins("JMP")
            self.next_token()
            self.eval.add_param(self.cur_token.text)
            self.match_type(TokenType.IDENT)
            self.eval.done()
        # "JEZ" ident
        elif self.check_type(TokenType.JEZ):
            self.eval.add_ins("JEZ")
            self.next_token()
            self.eval.add_param(self.cur_token.text)
            self.match_type(TokenType.IDENT)
            self.eval.done()
        # "JNZ" ident
        elif self.check_type(TokenType.JNZ):
            self.eval.add_ins("JNZ")
            self.next_token()
            self.eval.add_param(self.cur_token.text)
            self.match_type(TokenType.IDENT)
            self.eval.done()
        # "JGZ" ident
        elif self.check_type(TokenType.JGZ):
            self.eval.add_ins("JGZ")
            self.next_token()
            self.eval.add_param(self.cur_token.text)
            self.match_type(TokenType.IDENT)
            self.eval.done()
        # "JLZ" ident
        elif self.check_type(TokenType.JLZ):
            self.eval.add_ins("JLZ")
            self.next_token()
            self.eval.add_param(self.cur_token.text)
            self.match_type(TokenType.IDENT)
            self.eval.done()
        # "JRO" src
        elif self.check_type(TokenType.JRO):
            self.eval.add_ins("JRO")
            self.next_token()
            self.src()
            self.eval.done()
        # "PRINT" readable | string
        elif self.check_type(TokenType.PRINT):
            self.eval.add_ins("PRINT")
            self.next_token()
            if self.check_type(TokenType.STRING):
                self.eval.add_param(self.cur_token.text)
                self.next_token()
            else:
                self.readable()
            self.eval.done()
        else:
            self.print_and_exit(f"invalid token ({self.cur_token.text})")

        self.nl()


    def src(self):
        print("SRC")
        if self.check_type(TokenType.NUMBER):
            self.eval.add_param(self.cur_token.text)
            self.next_token()
        else:
            self.readable()

    def dst(self):
        print("DST")
        self.writable()

    def readable(self):
        print("READABLE")
        if self.check_type(TokenType.ACC):
            self.eval.add_param(self.cur_token.text)
            self.next_token()
        elif self.check_type(TokenType.IN):
            self.eval.add_param(self.cur_token.text)
            self.next_token()
        elif self.check_type(TokenType.STACK):
            self.eval.add_param(self.cur_token.text)
            self.next_token()
        else:
            self.print_and_exit(f"invalid token ({self.cur_token.text})")

    def writable(self):
        print("WRITABLE")
        if self.check_type(TokenType.ACC):
            self.eval.add_param(self.cur_token.text)
            self.next_token()
        elif self.check_type(TokenType.OUT):
            self.eval.add_param(self.cur_token.text)
            self.next_token()
        elif self.check_type(TokenType.STACK):
            self.eval.add_param(self.cur_token.text)
            self.next_token()
        elif self.check_type(TokenType.SCREEN):
            self.eval.add_param(self.cur_token.text)
            self.next_token()
        else:
            self.print_and_exit(f"invalid token ({self.cur_token.text})")

    def nl(self):
        print("NL")
        self.match_type(TokenType.NL)

        while self.check_type(TokenType.NL):
            self.next_token()
