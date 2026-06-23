from lexer import *
import sys

class Parser:
    # def __init__(self, lexer, eval):
    def __init__(self, lexer, state):
        self.lexer = lexer
        self.state = state
        # self.eval = eval

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

        if self.check_type(TokenType.NOP):
            ...
        elif self.check_type(TokenType.MOV):
            print("MOV")
            self.next_token()
            print(self.expression())
            self.match_type(TokenType.COMMA)
            print(",")
            self.dst()
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


    def dst(self):
        print("DST")
        if self.check_type(TokenType.ACC):
            print("ACC")
            self.next_token()
        elif self.check_type(TokenType.BP):
            self.next_token()
            self.match_type(TokenType.OPEN_PAREN)
            self.expression()
            self.match_type(TokenType.CLOSE_PAREN)
        elif self.check_type(TokenType.SP):
            self.next_token()
            self.match_type(TokenType.OPEN_PAREN)
            self.expression()
            self.match_type(TokenType.CLOSE_PAREN)
        elif self.check_type(TokenType.ASTERISK):
            self.next_token()
            if self.check_type(TokenType.BP):
                self.next_token()
                self.match_type(TokenType.OPEN_PAREN)
                self.expression()
                self.match_type(TokenType.CLOSE_PAREN)
            elif self.check_type(TokenType.SP):
                self.next_token()
                self.match_type(TokenType.OPEN_PAREN)
                self.expression()
                self.match_type(TokenType.CLOSE_PAREN)
            else:
                self.print_and_exit(f"invalid token ({self.cur_token.text})")
        else:
            self.print_and_exit(f"invalid token ({self.cur_token.text})")

    def expression(self):
        print("EXPRESSION")
        if self.check_type(TokenType.NUMBER):
            number_value = int(self.cur_token.text)
            self.next_token()
            return int(number_value)
        elif self.check_type(TokenType.NIL):
            self.next_token()
            return 0
        elif self.check_type(TokenType.ACC):
            print("ACC")
            self.next_token()
            return self.state.acc
        elif self.check_type(TokenType.IDENT):
            self.next_token()
            return self.state.consts[self.cur_token.text]
        # bp "(" expression ")"
        elif self.check_type(TokenType.BP):
            self.next_token()
            self.match_type(TokenType.OPEN_PAREN)
            expression_value = self.expression()
            self.match_type(TokenType.CLOSE_PAREN)
            # stack[bp + offset]
            return self.state.index(self.state.bp + expression_value)
        # sp "(" expression ")"
        elif self.check_type(TokenType.SP):
            self.next_token()
            self.match_type(TokenType.OPEN_PAREN)
            expression_value = self.expression()
            self.match_type(TokenType.CLOSE_PAREN)
            # stack[sp + offset]
            return self.state.index(self.state.sp + expression_value)
        elif self.check_type(TokenType.ASTERISK):
            self.next_token()
            # "*" bp "(" expression ")"
            if self.check_type(TokenType.BP):
                self.next_token()
                self.match_type(TokenType.OPEN_PAREN)
                expression_value = self.expression()
                self.match_type(TokenType.CLOSE_PAREN)
                # stack[stack[bp + offset]]
                return self.state.index(self.state.index(self.state.bp + expression_value))
            elif self.check_type(TokenType.SP):
                self.next_token()
                self.match_type(TokenType.OPEN_PAREN)
                expression_value = self.expression()
                self.match_type(TokenType.CLOSE_PAREN)
                # stack[stack[sp + offset]]
                return self.state.index(self.state.index(self.state.sp + expression_value))
            else:
list.insert(index, value, /)
Insert an item at a given position. The first argument is the index of the element before which to insert, so a.insert(0, x) inserts at the front of the list, and a.insert(len(a), x) is equivalent to a.append(x).

                self.print_and_exit(f"invalid token ({self.cur_token.text})")
        else:
            self.print_and_exit(f"invalid token ({self.cur_token.text})")

    def nl(self):
        print("NL")
        self.match_type(TokenType.NL)

        while self.check_type(TokenType.NL):
            self.next_token()
