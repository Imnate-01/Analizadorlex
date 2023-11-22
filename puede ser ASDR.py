class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.current_index = 0
        self.advance()

    def match(self, expected_token):
        if self.current_token == expected_token:
            self.advance()
        else:
            raise SyntaxError(f"Error: Expected {expected_token}, but got {self.current_token}")

    def advance(self):
        if self.current_index < len(self.tokens):
            self.current_token = self.tokens[self.current_index]
            self.current_index += 1
        else:
            self.current_token = None

    def program(self):
        self.declaration()

    def declaration(self):
        if self.current_token == "fun":
            self.function()
        elif self.current_token == "var":
            self.var_declaration()
        elif self.current_token in ["for", "if", "print", "return", "while", "{", "true", "false", "null", "number", "string", "id", "("]:
            self.statement()
        else:
            return

        self.declaration()

    def function(self):
        self.match("fun")
        self.match("id")
        self.match("(")
        self.parameters()
        self.match(")")
        self.block()

    def parameters(self):
        if self.current_token != ")":
            self.match("id")
            while self.current_token == ",":
                self.match(",")
                self.match("id")

    def block(self):
        self.match("{")
        self.declaration()
        self.match("}")

    def var_declaration(self):
        self.match("var")
        self.match("id")
        if self.current_token == "=":
            self.match("=")
            self.expression()

        self.match(";")

    def statement(self):
        if self.current_token == "for":
            self.for_statement()
        elif self.current_token == "if":
            self.if_statement()
        elif self.current_token == "print":
            self.print_statement()
        elif self.current_token == "return":
            self.return_statement()
        elif self.current_token == "while":
            self.while_statement()
        elif self.current_token == "{":
            self.block()
        else:
            self.expression()
            self.match(";")

    def for_statement(self):
        self.match("for")
        self.match("(")
        self.for_stmt_1()
        self.for_stmt_2()
        self.for_stmt_3()
        self.match(")")
        self.statement()

    def for_stmt_1(self):
        if self.current_token == "var":
            self.var_declaration()
        elif self.current_token == ";":
            self.match(";")
        else:
            self.expression()

    def for_stmt_2(self):
        if self.current_token != ";":
            self.expression()
        self.match(";")

    def for_stmt_3(self):
        if self.current_token != ")":
            self.expression()

    def if_statement(self):
        self.match("if")
        self.match("(")
        self.expression()
        self.match(")")
        self.statement()
        self.else_statement()

    def else_statement(self):
        if self.current_token == "else":
            self.match("else")
            self.statement()

    def print_statement(self):
        self.match("print")
        self.expression()
        self.match(";")

    def return_statement(self):
        self.match("return")
        if self.current_token != ";":
            self.expression()
        self.match(";")

    def while_statement(self):
        self.match("while")
        self.match("(")
        self.expression()
        self.match(")")
        self.statement()

    def expression(self):
        self.assignment()

    def assignment(self):
        self.logic_or()
        if self.current_token == "=":
            self.match("=")
            self.expression()

    def logic_or(self):
        self.logic_and()
        while self.current_token == "or":
            self.match("or")
            self.logic_and()

    def logic_and(self):
        self.equality()
        while self.current_token == "and":
            self.match("and")
            self.equality()

    def equality(self):
        self.comparison()
        while self.current_token in ["==", "!="]:
            self.match(self.current_token)
            self.comparison()

    def comparison(self):
        self.term()
        while self.current_token in [">", ">=", "<", "<="]:
            self.match(self.current_token)
            self.term()

    def term(self):
        self.factor()
        while self.current_token in ["+", "-"]:
            self.match(self.current_token)
            self.factor()

    def factor(self):
        self.unary()
        while self.current_token in ["*", "/"]:
            self.match(self.current_token)
            self.unary()

    def unary(self):
        if self.current_token in ["!", "-"]:
            self.match(self.current_token)
            self.unary()
        else:
            self.call()

    def call(self):
        self.primary()
        self.call_2()

    def call_2(self):
        if self.current_token == "(":
            self.match("(")
            self.arguments_opc()
            self.match(")")
            self.call_2()

    def primary(self):
        if self.current_token in ["true", "false", "null", "number", "string", "id"]:
            self.match(self.current_token)
        elif self.current_token == "(":
            self.match("(")
            self.expression()
            self.match(")")
        else:
            raise SyntaxError("Error: Expected primary expression")

    def arguments_opc(self):
        if self.current_token != ")":
            self.expression()
            self.arguments()

    def arguments(self):
        if self.current_token == ",":
            self.match(",")
            self.expression()
            self.arguments()


while True:
    input_string = input(">>>")
    if input_string.lower() == 'exit':
        break

    tokens = input_string.split()
    parser = Parser(tokens)

    try:
        parser.program()
        print("La entrada es válida.")
    except SyntaxError as e:
        print(e)
        print("La entrada no es válida.")
