class SQLParser:
    def __init__(self, consulta):
        # Inicializa el analizador con la consulta proporcionada
        self.tokens = consulta.split()
        self.token_actual = None
        self.indice = 0
        self.pila = [] 
 def siguiente_token(self):
        # Avanza al siguiente token en la lista de tokens
        if self.indice < len(self.tokens):
            self.token_actual = self.tokens[self.indice]
            self.indice += 1
        else:
            self.token_actual = None

    def coincidir(self, token_esperado):
        # Comprueba si el token actual coincide con el esperado
        if self.token_actual == token_esperado:
            self.siguiente_token()
        else:
            raise ValueError(f"Error de sintaxis. Se esperaba '{token_esperado}' pero se encontró '{self.token_actual}'.")
