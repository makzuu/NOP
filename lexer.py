from enum import Enum
import sys

class TokenType(Enum):
    EOF     = -1
    NL      = 0
    COMMA   = 1
    COLON   = 2

    # Keywords
    MOV     = 101
    SWP     = 102
    SAV     = 103
    ADD     = 104
    SUB     = 105
    NEG     = 106
    JMP     = 107
    JEZ     = 108
    JNZ     = 109
    JGZ     = 110
    JLZ     = 111
    JRO     = 112
    PRINT   = 113
    ACC     = 114
    IN      = 115
    OUT     = 116
    STACK   = 117
    SCREEN  = 118

    IDENT   = 201
    STRING  = 202
    NUMBER  = 203


class Token:
    def __init__(self, token_text, token_type, line):
        self.text = token_text
        self.type = token_type
        self.line = line

    @staticmethod
    def is_keyword(text):
        for token_type in TokenType:
            if text == token_type.name and token_type.value > 100 and token_type.value < 200:
                return token_type
        return None


class Lexer:
    def __init__(self, source):
        self.source = source + "\n"

        self.cur_pos = -1
        self.cur_char = ""
        self.cur_line = 1

        self.next_char()

    def next_char(self):
        self.cur_pos += 1
        if self.cur_pos >= len(self.source):
            self.cur_char = "\0"
        else:
            self.cur_char = self.source[self.cur_pos]

    def peek_char(self):
        if self.cur_pos + 1 >= len(self.source):
            return "\0"
        return self.source[self.cur_pos + 1]

    def skip_whitespace(self):
        while self.cur_char == " " or self.cur_char == "\t" or self.cur_char == "\r":
            self.next_char()

    def skip_comments(self):
        if self.cur_char == "#":
            while self.cur_char != "\n":
                self.next_char()

    def get_token(self):
        self.skip_whitespace()
        self.skip_comments()

        token = None

        if self.cur_char == "\0":
            token = Token("", TokenType.EOF, self.cur_line)
        elif self.cur_char == "\n":
            token = Token("", TokenType.NL, self.cur_line)
            self.cur_line += 1
        elif self.cur_char == ",":
            token = Token(self.cur_char, TokenType.COMMA, self.cur_line)
        elif self.cur_char == ":":
            token = Token(self.cur_char, TokenType.COLON, self.cur_line)
        elif self.cur_char.isdigit():
            start_pos = self.cur_pos
            while self.peek_char().isdigit():
                self.next_char()
            token = Token(self.source[start_pos : self.cur_pos + 1], TokenType.NUMBER, self.cur_line)
        elif self.cur_char == "-":
            start_pos = self.cur_pos
            while self.peek_char().isdigit():
                self.next_char()
            token_text = self.source[start_pos : self.cur_pos + 1]
            if len(token_text) < 2:
                sys.exit(f"expected number found ({self.peek_char()})")
            token = Token(token_text, TokenType.NUMBER, self.cur_line)
        elif self.cur_char == "\"":
            start_pos = self.cur_pos + 1
            while self.peek_char() != "\"" and self.peek_char() != "\n":
                self.next_char()
            if self.peek_char() == "\"":
                token = Token(self.source[start_pos : self.cur_pos + 1], TokenType.STRING, self.cur_line)
                self.next_char()
            else:
                sys.exit(f"expected (\") found ({self.peek_char()})")
        elif self.cur_char.isalpha():
            start_pos = self.cur_pos
            while self.peek_char().isalnum():
                self.next_char()

            token_text = self.source[start_pos : self.cur_pos + 1]
            token_type = Token.is_keyword(token_text)

            if token_type != None:
                token = Token(token_text, token_type, self.cur_line)
            else:
                token = Token(token_text, TokenType.IDENT, self.cur_line)
        else:
            sys.exit(f"Unkown token ({self.cur_char})")

        self.next_char()

        return token
