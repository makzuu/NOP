import logger as log
from tok import *


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
            token = Token("EOF", TokenType.EOF, self.cur_line)
        elif self.cur_char == "\n":
            token = Token("NL", TokenType.NL, self.cur_line)
            self.cur_line += 1
        elif self.cur_char == ",":
            token = Token(self.cur_char, TokenType.COMMA, self.cur_line)
        elif self.cur_char == ":":
            token = Token(self.cur_char, TokenType.COLON, self.cur_line)
        elif self.cur_char == "*":
            token = Token(self.cur_char, TokenType.ASTERISK, self.cur_line)
        elif self.cur_char == "(":
            token = Token(self.cur_char, TokenType.OPEN_PAREN, self.cur_line)
        elif self.cur_char == ")":
            token = Token(self.cur_char, TokenType.CLOSE_PAREN, self.cur_line)
        elif self.cur_char.isdigit() or self.cur_char == "-":
            start_pos = self.cur_pos
            while self.peek_char().isdigit():
                self.next_char()
            token_text = self.source[start_pos : self.cur_pos + 1]
            if token_text == "-":
                log.error(f"({self.peek_char()}) is not a number")
            token = Token(token_text, TokenType.NUMBER, self.cur_line)
        elif self.cur_char.isalpha() or self.cur_char == "_":
            start_pos = self.cur_pos
            while self.peek_char().isalnum() or self.peek_char() == "_":
                self.next_char()

            token_text = self.source[start_pos : self.cur_pos + 1]
            token_type = Token.is_keyword(token_text)

            if token_type != None:
                token = Token(token_type.name, token_type, self.cur_line)
            else:
                token = Token(token_text, TokenType.IDENT, self.cur_line)
        else:
            log.error(f"Unkown token ({self.cur_char})")

        self.next_char()

        return token
