from lexer import Lexer
from tok import TokenType
import pytest


def test_basic_usage():
    code = """
    MOV 1, ACC
    WRITE ACC
    """
    expected_output = [
        TokenType.NL,
        TokenType.MOV,
        TokenType.NUMBER,
        TokenType.COMMA,
        TokenType.ACC,
        TokenType.NL,
        TokenType.WRITE,
        TokenType.ACC,
        TokenType.NL,
        TokenType.NL,
        TokenType.EOF,
        TokenType.EOF,
    ]
    lex = Lexer(code)
    for token_type in expected_output:
        token = lex.get_token()
        assert token.type == token_type


def test_unkown_token():
    code = "MOV ?, ACC"
    lex = Lexer(code)
    lex.get_token()  # skip MOV token
    with pytest.raises(SystemExit):
        token = lex.get_token()
