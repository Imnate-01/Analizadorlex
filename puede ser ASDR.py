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
            raise SyntaxError(f"Error: Se esperaba {expected_token}, pero se obtuvo {self.current_token}")

    def advance(self):
        if self.current_index < len(self.tokens):
            self.current_token = self.tokens[self.current_index]
            self.current_index += 1
        else:
            self.current_token = None

    def program(self):
        self.declaracion()

    def declaracion(self):
        if self.current_token == "fun":
            self.funcion()
        elif self.current_token == "var":
            self.declaracion_var()
        elif self.current_token in ["for", "if", "print", "return", "while", "{", "true", "false", "null", "number", "string", "id", "("]:
            self.sentencia()
        else:
            return

        self.declaracion()

    def funcion(self):
        self.match("fun")
        self.match("id")
        self.match("(")
        self.parametros()
        self.match(")")
        self.bloque()

    def parametros(self):
        if self.current_token != ")":
            self.match("id")
            while self.current_token == ",":
                self.match(",")
                self.match("id")

    def bloque(self):
        self.match("{")
        self.declaracion()
        self.match("}")

    def declaracion_var(self):
        self.match("var")
        self.match("id")
        if self.current_token == "=":
            self.match("=")
            self.expresion()

        self.match(";")

    def sentencia(self):
        if self.current_token == "for":
            self.sentencia_for()
        elif self.current_token == "if":
            self.sentencia_if()
        elif self.current_token == "print":
            self.sentencia_print()
        elif self.current_token == "return":
            self.sentencia_return()
        elif self.current_token == "while":
            self.sentencia_while()
        elif self.current_token == "{":
            self.bloque()
        else:
            self.expresion()
            self.match(";")

    def sentencia_for(self):
        self.match("for")
        self.match("(")
        self.sentencia_for_1()
        self.sentencia_for_2()
        self.sentencia_for_3()
        self.match(")")
        self.sentencia()

    def sentencia_for_1(self):
        if self.current_token == "var":
            self.declaracion_var()
        elif self.current_token == ";":
            self.match(";")
        else:
            self.expresion()

    def sentencia_for_2(self):
        if self.current_token != ";":
            self.expresion()
        self.match(";")

    def sentencia_for_3(self):
        if self.current_token != ")":
            self.expresion()

    def sentencia_if(self):
        self.match("if")
        self.match("(")
        self.expresion()
        self.match(")")
        self.sentencia()
        self.sentencia_else()

    def sentencia_else(self):
        if self.current_token == "else":
            self.match("else")
            self.sentencia()

    def sentencia_print(self):
        self.match("print")
        self.expresion()
        self.match(";")

    def sentencia_return(self):
        self.match("return")
        if self.current_token != ";":
            self.expresion()
        self.match(";")

    def sentencia_while(self):
        self.match("while")
        self.match("(")
        self.expresion()
        self.match(")")
        self.sentencia()

    def expresion(self):
        self.asignacion()

    def asignacion(self):
        self.logica_o()
        if self.current_token == "=":
            self.match("=")
            self.expresion()

    def logica_o(self):
        self.logica_y()
        while self.current_token == "or":
            self.match("or")
            self.logica_y()

    def logica_y(self):
        self.igualdad()
        while self.current_token == "and":
            self.match("and")
            self.igualdad()

    def igualdad(self):
        self.comparacion()
        while self.current_token in ["==", "!="]:
            self.match(self.current_token)
            self.comparacion()

    def comparacion(self):
        self.termino()
        while self.current_token in [">", ">=", "<", "<="]:
            self.match(self.current_token)
            self.termino()

    def termino(self):
        self.factor()
        while self.current_token in ["+", "-"]:
            self.match(self.current_token)
            self.factor()

    def factor(self):
        self.unario()
        while self.current_token in ["*", "/"]:
            self.match(self.current_token)
            self.unario()

    def unario(self):
        if self.current_token in ["!", "-"]:
            self.match(self.current_token)
            self.unario()
        else:
            self.llamada()

    def llamada(self):
        self.principal()
        self.llamada_2()

    def llamada_2(self):
        if self.current_token == "(":
            self.match("(")
            self.argumentos_opc()
            self.match(")")
            self.llamada_2()

    def principal(self):
        if self.current_token in ["true", "false", "null", "number", "string", "id"]:
            self.match(self.current_token)
        elif self.current_token == "(":
            self.match("(")
            self.expresion()
            self.match(")")
        else:
            raise SyntaxError("Error: Se esperaba una expresión primaria")

    def argumentos_opc(self):
        if self.current_token != ")":
            self.expresion()
            self.argumentos()

    def argumentos(self):
        if self.current_token == ",":
            self.match(",")
            self.expresion()
            self.argumentos()


# Bucle principal
while True:
    input_string = input(">>> ")
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
