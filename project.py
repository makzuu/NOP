import sys
from lexer import *

def main():
    if len(sys.argv) < 2:
        sys.exit(f"usage: {sys.argv[0]} <program>")
    source = get_source(sys.argv[1])
    lex = Lexer(source)

    token = lex.get_token()
    while token.type != TokenType.EOF:
        print(token.type, token.text)
        token = lex.get_token()



def get_source(filename):
    try:
        with open(filename) as f:
            source = f.read()
    except FileNotFoundError:
        sys.exit(f"file {filename} does not exist")
    return source


if __name__ == "__main__":
    main()
