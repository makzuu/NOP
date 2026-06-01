from lexer import *
import sys

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer

        self.cur_token = None
        self.next_token()

    def check_type(self, type):
        return self.cur_token.type == type

    def match_type(self, type):
        if self.cur_token.type == type:
            self.next_token()
        else:
            sys.exit(f"invalid token {self.cur_token.text}")

    def next_token(self):
        self.cur_token = self.lexer.get_token()

    def program(self):
        print("PROGRAM")
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
            self.next_token()
            self.match_type(TokenType.COLON)
        # "MOV" src "," dst
        elif self.check_type(TokenType.MOV):
            self.next_token()
            self.src()
            self.match_type(TokenType.COMMA)
            self.dst()
        # "SWP"
        elif self.check_type(TokenType.SWP):
            self.next_token()
        # "SAV"
        elif self.check_type(TokenType.SAV):
            self.next_token()
        # "ADD" src
        elif self.check_type(TokenType.ADD):
            self.next_token()
            self.src()
        # "SUB" src
        elif self.check_type(TokenType.SUB):
            self.next_token()
            self.src()
        # "NEG"
        elif self.check_type(TokenType.NEG):
            self.next_token()
        # "JMP" ident
        elif self.check_type(TokenType.JMP):
            self.next_token()
            self.match_type(TokenType.IDENT)
        # "JEZ" ident
        elif self.check_type(TokenType.JEZ):
            self.next_token()
            self.match_type(TokenType.IDENT)
        # "JNZ" ident
        elif self.check_type(TokenType.JNZ):
            self.next_token()
            self.match_type(TokenType.IDENT)
        # "JGZ" ident
        elif self.check_type(TokenType.JGZ):
            self.next_token()
            self.match_type(TokenType.IDENT)
        # "JLZ" ident
        elif self.check_type(TokenType.JLZ):
            self.next_token()
            self.match_type(TokenType.IDENT)
        # "JRO" src
        elif self.check_type(TokenType.JRO):
            self.next_token()
            self.src()
        # "PRINT" readable | string
        elif self.check_type(TokenType.PRINT):
            self.next_token()
            if self.check_type(TokenType.STRING):
                self.next_token()
            else:
                self.readable()
        else:
            sys.exit(f"invalid token {self.cur_token.text}")

        self.nl()


    def src(self):
        print("SRC")
        if self.check_type(TokenType.NUMBER):
            self.next_token()
        else:
            self.readable()

    def dst(self):
        print("DST")
        self.writable()

    def readable(self):
        print("READABLE")
        if self.check_type(TokenType.ACC):
            self.next_token()
        elif self.check_type(TokenType.IN):
            self.next_token()
        elif self.check_type(TokenType.STACK):
            self.next_token()
        else:
            sys.exit(f"invalid token {self.cur_token.text}")

    def writable(self):
        print("WRITABLE")
        if self.check_type(TokenType.ACC):
            self.next_token()
        elif self.check_type(TokenType.OUT):
            self.next_token()
        elif self.check_type(TokenType.STACK):
            self.next_token()
        elif self.check_type(TokenType.SCREEN):
            self.next_token()
        else:
            sys.exit(f"invalid token {self.cur_token.text}")

    def nl(self):
        print("NL")
        self.match_type(TokenType.NL)

        while self.check_type(TokenType.NL):
            self.next_token()
