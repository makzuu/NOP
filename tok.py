from enum import Enum


class TokenType(Enum):
    EOF                 =  -1
    NL                  =   0
    COMMA               =   1
    COLON               =   2
    ASTERISK            =   3
    OPEN_PAREN          =   4
    CLOSE_PAREN         =   5

    # Keywords
    NOP                 = 101
    MOV                 = 102
    SWP                 = 103
    SAV                 = 104
    ADD                 = 105
    SUB                 = 106
    NEG                 = 107
    JMP                 = 108
    JEZ                 = 109
    JNZ                 = 110
    JGZ                 = 111
    JLZ                 = 112
    JRO                 = 113

    PUSH                = 114
    POP                 = 115
    READ                = 116
    WRITE               = 117
    DEFINE              = 118
    CALL                = 119
    RET                 = 120
    DRAW                = 121

    ACC                 = 122
    NIL                 = 123
    BP                  = 124
    SP                  = 125

    IDENT               = 201
    NUMBER              = 202


class Token:
    def __init__(self, token_text, token_type, line):
        self.text = token_text
        self.type = token_type
        self.line = line

    @staticmethod
    def is_keyword(text):
        for token_type in TokenType:
            if text.lower() == token_type.name.lower() and token_type.value > 100 and token_type.value < 200:
                return token_type
        return None
