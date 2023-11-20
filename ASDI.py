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
def analizar(self):
        # Inicia el análisis sintáctico
        self.siguiente_token()

        while True:
            # Manejo de la cláusula SELECT
            if self.token_actual.lower() == "select":
                self.pila.append("select")
                self.siguiente_token()
                while self.token_actual.lower() == "distinct":
                    self.coincidir("distinct")
                if self.token_actual == "*":








def main():
    while True:
        # Solicita al usuario que introduzca una consulta SQL
        consulta = input("Introduce una cadena SQL (o 'exit' para salir): ")

        if consulta.lower() == 'exit':
            break

        consulta += ' $'  # Agrega el símbolo $ al final de la cadena
        analizador = SQLParser(consulta)

        try:
            analizador.analizar()
        except Exception as e:
            # Captura y maneja cualquier error durante el análisis
            print(f"Error al analizar la consulta: {e}")


if __name__ == "__main__":
    main()
                    self.coincidir("*")
