import re
import enum
import sys 
class TipoToken(enum.Enum):
    LEFT_PAREN = 'LEFT_PAREN'
    RIGHT_PAREN = 'RIGHT_PAREN'
    LEFT_BRACE = 'LEFT_BRACE'
    RIGHT_BRACE = 'RIGHT_BRACE'
    COMMA = 'COMMA'
    DOT = 'DOT'
    MINUS = 'MINUS'
    PLUS = 'PLUS'
    SEMICOLON = 'SEMICOLON'
    SLASH = 'SLASH'
    STAR = 'STAR'
    BANG = 'BANG'
    BANG_EQUAL = 'BANG_EQUAL'
    EQUAL = 'EQUAL'
    EQUAL_EQUAL = 'EQUAL_EQUAL'
    GREATER = 'GREATER'
    GREATER_EQUAL = 'GREATER_EQUAL'
    LESS = 'LESS'
    LESS_EQUAL = 'LESS_EQUAL'
    IDENTIFIER = 'IDENTIFIER'
    STRING = 'STRING'
    NUMBER = 'NUMBER'
    AND = 'AND'
    ELSE = 'ELSE'
    FALSE = 'FALSE'
    FUN = 'FUN'
    FOR = 'FOR'
    IF = 'IF'
    NULL = 'NULL'
    OR = 'OR'
    PRINT = 'PRINT'
    RETURN = 'RETURN'
    TRUE = 'TRUE'
    VAR = 'VAR'
    WHILE = 'WHILE'
    EOF = 'EOF'

class Token:
    def __init__(self, tipo, lexema, literal=None):
        self.tipo = tipo
        self.lexema = lexema
        self.literal = literal

class Lexer:
    def __init__(self, codigo):
        self.codigo = codigo
        self.posicion = 0
        self.linea = 1
        self.columna = 1
        self.tokens = []

    def scan_tokens(self):
        while self.posicion < len(self.codigo):
            self.inicio = self.posicion
            self.scan_token()

        self.tokens.append(Token(TipoToken.EOF, '', None))
        return self.tokens

    def scan_token(self):
        c = self.advance()
        if c == '(':
            self.add_token(TipoToken.LEFT_PAREN)
        elif c == ')':
            self.add_token(TipoToken.RIGHT_PAREN)
        elif c == '{':
            self.add_token(TipoToken.LEFT_BRACE)
        elif c == '}':
            self.add_token(TipoToken.RIGHT_BRACE)
        elif c == ',':
            self.add_token(TipoToken.COMMA)
        elif c == '.':
            self.add_token(TipoToken.DOT)
        elif c == '-':
            self.add_token(TipoToken.MINUS)
        elif c == '+':
            self.add_token(TipoToken.PLUS)
        elif c == ';':
            self.add_token(TipoToken.SEMICOLON)
        elif c == '*':
            self.add_token(TipoToken.STAR)
        elif c == '!':
            if self.match('='):
                self.add_token(TipoToken.BANG_EQUAL)
            else:
                self.add_token(TipoToken.BANG)
        elif c == '=':
            if self.match('='):
                self.add_token(TipoToken.EQUAL_EQUAL)
            else:
                self.add_token(TipoToken.EQUAL)
        elif c == '<':
            if self.match('='):
                self.add_token(TipoToken.LESS_EQUAL)
            else:
                self.add_token(TipoToken.LESS)
        elif c == '>':
            if self.match('='):
                self.add_token(TipoToken.GREATER_EQUAL)
            else:
                self.add_token(TipoToken.GREATER)
        elif c == '/':
            if self.match('/'):
                while self.peek() != '\n' and not self.is_at_end():
                    self.advance()
            elif self.match('*'):
                while True:
                    if self.is_at_end():
                        print("Comentario multilínea no cerrado")
                        break
                    if self.peek() == '*' and self.peek_next() == '/':
                        self.advance()
                        self.advance()
                        break
                    self.advance()
            else:
                self.add_token(TipoToken.SLASH)
        elif c == ' ' or c == '\t' or c == '\r':
            pass
        elif c == '\n':
            self.linea += 1
            self.columna = 1
        elif c == '"':
            self.string()
        elif c.isdigit():
            self.number()
        elif c.isalpha() or c == '_':
            self.identifier()
        else:
            raise Exception(f"Caracter inesperado '{c}' en línea {self.linea}, columna {self.columna}")

    def advance(self):
        c = self.codigo[self.posicion]
        self.posicion += 1
        self.columna += 1
        return c

    def match(self, expected):
        if self.is_at_end() or self.codigo[self.posicion] != expected:
            return False
        self.posicion += 1
        self.columna += 1
        return True

    def peek(self):
        if self.is_at_end():
            return '\0'
        return self.codigo[self.posicion]

    def is_at_end(self):
        return self.posicion >= len(self.codigo)

    def add_token(self, tipo, literal=None):
        lexema = self.codigo[self.inicio:self.posicion]
        self.tokens.append(Token(tipo, lexema, literal))

    def string(self):
        start = self.posicion
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.linea += 1
                self.columna = 1
            self.advance()

        if self.is_at_end():
            raise Exception("Cadena no cerrada")

        self.advance()

        lexema = self.codigo[start:self.posicion]
        literal = self.codigo[start + 1:self.posicion - 1]  
        self.add_token(TipoToken.STRING, literal)

    def number(self):
        start = self.posicion
        while self.peek().isdigit():
            self.advance()

        if self.peek() == '.':
            self.advance()
            while self.peek().isdigit():
                self.advance()

        if self.peek() in ('e', 'E'):
            self.advance()
            if self.peek() in ('+', '-'):
                self.advance()
            while self.peek().isdigit():
                self.advance()

        lexema = self.codigo[start:self.posicion]
    
        try:
            if '.' in lexema or 'e' in lexema or 'E' in lexema:
                literal = float(lexema)
            else:
                literal = int(lexema)
        except ValueError:
            literal = None

        self.add_token(TipoToken.NUMBER, literal)


    def slash(self):
        lexema = self.advance()
        self.add_token(TipoToken.SLASH, lexema)


    def plus(self):
        lexema = self.advance()
        self.add_token(TipoToken.PLUS, lexema)


    def identifier(self):
        while self.peek().isalnum() or self.peek() == '_':
            self.advance()

        lexema = self.codigo[self.inicio:self.posicion]
        if lexema in reserved_words:
            token_type = TipoToken[lexema.upper()]
        else:
            token_type = TipoToken.IDENTIFIER

        self.add_token(token_type)

    def peek_next(self):
        if self.posicion + 1 >= len(self.codigo):
            return '\0'
        return self.codigo[self.posicion + 1]

reserved_words = {
    'AND', 'ELSE', 'FALSE', 'FOR', 'FUN', 'IF', 'NULL', 'OR',
    'PRINT', 'RETURN', 'TRUE', 'VAR', 'WHILE','and', 'else', 'false', 
'for', 'fun', 'if', 'null', 'or', 'print', 'return', 'true', 'var', 'while'
}

def main():
    if len(sys.argv) > 1:
        for archivo in sys.argv[1:]:
            try:
                with open(archivo, 'r') as f:
                    codigo = f.read()
                    lexer = Lexer(codigo)
                    tokens = lexer.scan_tokens()
                    for token in tokens:
                        print(f'{token.tipo.value}: {token.lexema} ({token.literal})')
            except FileNotFoundError:
                print(f"El archivo '{archivo}' no se encontró.")
    else:
        while True:
            try:
                codigo = input(">>> ").strip()
                if codigo.lower() == 'q':
                    break
                lexer = Lexer(codigo)
                tokens = lexer.scan_tokens()
                for token in tokens:
                    print(f'{token.tipo.value}: {token.lexema} ({token.literal})')
            except KeyboardInterrupt:
                print("\nSaliendo de la aplicación.")
                break

if __name__ == "__main__":
    main()

