import logger as log
from token import TokenType

class Node:
    def __init__(self, token=None):
        self.children = []
        self.token = token

class Parser:
    def __init__(self, lexer, state, eval):
        self.lexer = lexer
        self.state = state
        self.eval = eval

        self.tree = Node()
        self.cur_node = self.tree

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

    def add_node(self, node):
        self.cur_node.children.append(node)
    
    @staticmethod
    def print_tree(node, depth=0):
        if node.token != None:
            print("\t" * depth, str(node.token.text))
        for child in node.children:
            Parser.print_tree(child, depth+1)

    def program(self):
        self.skip_nl()

        while self.cur_token.type != TokenType.EOF:
            self.statement()

        Parser.print_tree(self.tree)

    def statement(self):
        self.cur_node = self.tree
        if self.check_type(TokenType.NOP):
            self.add_node(Node(self.cur_token))
            self.next_token()
        elif self.check_type(TokenType.MOV):
            node = Node(self.cur_token)
            self.add_node(node)
            self.cur_node = node
            self.next_token()
            self.src()
            self.match_type(TokenType.COMMA)
            self.cur_node = node
            self.dst()
        elif self.check_type(TokenType.SWP):
            self.add_node(Node(self.cur_token))
            self.next_token()
        elif self.check_type(TokenType.SAV):
            self.add_node(Node(self.cur_token))
            self.next_token()
        elif self.check_type(TokenType.ADD):
            node = Node(self.cur_token)
            self.add_node(node)
            self.cur_node = node
            self.next_token()
            self.src()
        elif self.check_type(TokenType.SUB):
            node = Node(self.cur_token)
            self.add_node(node)
            self.cur_node = node
            self.next_token()
            self.src()
        elif self.check_type(TokenType.NEG):
            self.add_node(Node(self.cur_token))
            self.next_token()
        elif self.check_type(TokenType.JMP):
            node = Node(self.cur_token)
            self.add_node(node)
            self.next_token()
            node.children.append(Node(self.cur_token))
            self.match_type(TokenType.IDENT)
        elif self.check_type(TokenType.JEZ):
            node = Node(self.cur_token)
            self.add_node(node)
            self.next_token()
            node.children.append(Node(self.cur_token))
            self.match_type(TokenType.IDENT)
        elif self.check_type(TokenType.JNZ):
            node = Node(self.cur_token)
            self.add_node(node)
            self.next_token()
            node.children.append(self.cur_token)
            self.match_type(TokenType.IDENT)
        elif self.check_type(TokenType.JGZ):
            node = Node(self.cur_token)
            self.add_node(node)
            self.next_token()
            node.children.append(self.cur_token)
            self.match_type(TokenType.IDENT)
        elif self.check_type(TokenType.JLZ):
            node = Node(self.cur_token)
            self.add_node(node)
            self.next_token()
            node.children.append(self.cur_token)
            self.match_type(TokenType.IDENT)
        elif self.check_type(TokenType.JRO):
            node = Node(self.cur_token)
            self.add_node(node)
            self.cur_node = node
            self.next_token()
            self.src()
        # | ident ":"
        elif self.check_type(TokenType.IDENT):
            self.add_node(Node(self.cur_token))
            self.next_token()
            self.match_type(TokenType.COLON)
            if self.check_type(TokenType.NL):
                self.nl()
            return
        elif self.check_type(TokenType.PUSH):
            node = Node(self.cur_token)
            self.add_node(node)
            self.cur_node = node
            self.next_token()
            self.src()
        elif self.check_type(TokenType.POP):
            node = Node(self.cur_token)
            self.add_node(node)
            self.cur_node = node
            self.next_token()
            self.dst()
        elif self.check_type(TokenType.READ):
            self.add_node(Node(self.cur_token))
            self.next_token()
        elif self.check_type(TokenType.WRITE):
            node = Node(self.cur_token)
            self.add_node(node)
            self.cur_node = node
            self.next_token()
            self.src()
        elif self.check_type(TokenType.DEFINE):
            node = Node(self.cur_token)
            self.add_node(node)
            self.cur_node = node
            self.next_token()
            self.add_node(Node(self.cur_token))
            self.match_type(TokenType.IDENT)
            self.match_type(TokenType.COMMA)
            self.add_node(Node(self.cur_token))
            self.match_type(TokenType.NUMBER)
        elif self.check_type(TokenType.CALL):
            node = Node(self.cur_token)
            self.add_node(node)
            self.cur_node = node
            self.next_token()
            self.add_node(Node(self.cur_token))
            self.match_type(TokenType.IDENT)
        elif self.check_type(TokenType.RET):
            self.add_node(Node(self.cur_token))
            self.next_token()
        elif self.check_type(TokenType.DRAW):
            self.add_node(Node(self.cur_token))
            self.next_token()
        else:
            log.error(f"invalid token ({self.cur_token.text})", self.cur_token.line)

        self.nl()

    def src(self):
        node = Node()
        self.add_node(node)
        self.cur_node = node
        if self.check_type(TokenType.ACC):
            self.add_node(Node(self.cur_token))
            self.next_token()
        elif self.check_type(TokenType.NIL):
            self.add_node(Node(self.cur_token))
            self.next_token()
        elif self.check_type(TokenType.NUMBER):
            self.add_node(Node(self.cur_token))
            self.next_token()
        elif self.check_type(TokenType.IDENT):
            self.add_node(Node(self.cur_token))
            self.next_token()
        elif self.check_type(TokenType.BP):
            self.add_node(Node(self.cur_token))
            self.next_token()
            if self.check_type(TokenType.OPEN_BRACKET):
                self.next_token()
                self.src()
                self.match_type(TokenType.CLOSE_BRACKET)
        elif self.check_type(TokenType.SP):
            self.add_node(Node(self.cur_token))
            self.next_token()
            if self.check_type(TokenType.OPEN_BRACKET):
                self.next_token()
                self.src()
                self.match_type(TokenType.CLOSE_BRACKET)
        else:
            log.error(f"invalid token ({self.cur_token.text})", self.cur_token.line)

    def dst(self):
        node = Node()
        self.add_node(node)
        self.cur_node = node
        if self.check_type(TokenType.ACC):
            self.add_node(Node(self.cur_token))
            self.next_token()
        elif self.check_type(TokenType.NIL):
            self.add_node(Node(self.cur_token))
            self.next_token()
        elif self.check_type(TokenType.IDENT):
            self.add_node(Node(self.cur_token))
            self.next_token()
        elif self.check_type(TokenType.BP):
            self.add_node(Node(self.cur_token))
            self.next_token()
            if self.check_type(TokenType.OPEN_BRACKET):
                self.next_token()
                self.src()
                self.match_type(TokenType.CLOSE_BRACKET)
        elif self.check_type(TokenType.SP):
            self.add_node(Node(self.cur_token))
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
