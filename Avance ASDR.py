class ParserException(Exception):
    pass

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0
        self.preanalisis = self.tokens[0]

    # Asumiendo que las implementaciones de term2, argumentsOptional, y expression
    

    def term(self):
        self.factor()
        self.term2()

    def factor(self):
        expr = self.unary()
        return self.factor2(expr)

    def factor2(self, expr):
        if self.preanalisis.tipo == TipoToken.SLASH:
            self.match(TipoToken.SLASH)
            operador = self.previous()
            expr2 = self.unary()
            expb = ExprBinary(expr, operador, expr2)
            return self.factor2(expb)
        elif self.preanalisis.tipo == TipoToken.STAR:
            self.match(TipoToken.STAR)
            operador = self.previous()
            expr2 = self.unary()
            expb = ExprBinary(expr, operador, expr2)
            return self.factor2(expb)
        return expr

    def unary(self):
        if self.preanalisis.tipo == TipoToken.BANG:
            self.match(TipoToken.BANG)
            operador = self.previous()
            expr = self.unary()
            return ExprUnary(operador, expr)
        elif self.preanalisis.tipo == TipoToken.MINUS:
            self.match(TipoToken.MINUS)
            operador = self.previous()
            expr = self.unary()
            return ExprUnary(operador, expr)
        else:
            return self.call()

    def call(self):
        expr = self.primary()
        return self.call2(expr)

    def call2(self, expr):
        if self.preanalisis.tipo == TipoToken.LEFT_PAREN:
            self.match(TipoToken.LEFT_PAREN)
            lstArguments = self.argumentsOptional()
            self.match(TipoToken.RIGHT_PAREN)
            ecf = ExprCallFunction(expr, lstArguments)
            return self.call2(ecf)
        return expr

    def primary(self):
        if self.preanalisis.tipo == TipoToken.TRUE:
            self.match(TipoToken.TRUE)
            return ExprLiteral(True)
        # ... y así sucesivamente para los otros casos

    def match(self, tt):
        if self.preanalisis.tipo == tt:
            self.i += 1
            self.preanalisis = self.tokens[self.i]
        else:
            message = f"Error en la línea {self.preanalisis.position.line}. " \
                      f"Se esperaba {self.preanalisis.tipo}, pero se encontró {tt}"
            raise ParserException(message)

    def previous(self):
        return self.tokens[self.i - 1]

