class SQLParser:
    def __init__(self, consulta):
        self.tokens = consulta.split()
        self.token_actual = None
        self.indice = 0
        self.pila = ["$", "Q"]  # Inicia la pila en el estado Q
        self.siguiente_token()

    def siguiente_token(self):
        if self.indice < len(self.tokens):
            self.token_actual = self.tokens[self.indice]
            self.indice += 1
        else:
            self.token_actual = "$"

    def coincidir(self, token_esperado):
        if self.token_actual == token_esperado:
            self.siguiente_token()
        else:
            raise ValueError(f"Error de sintaxis. Se esperaba '{token_esperado}' pero se encontró '{self.token_actual}'.")

    def analizar(self):
        while self.pila:
            estado_actual = self.pila.pop()

            if estado_actual == "$" and self.token_actual == "$":
                print("La consulta es sintácticamente válida.")
                break

            if estado_actual == "Q":
                if self.token_actual.lower() == "select":
                    self.pila.append("T")
                    self.pila.append("from")
                    self.pila.append("D")
                    self.pila.append("select")
                else:
                    raise ValueError(f"Error de sintaxis. Se esperaba 'select' pero se encontró '{self.token_actual}'.")
            elif estado_actual == "select":
                self.coincidir("select")
            elif estado_actual == "from":
                self.coincidir("from")
                self.pila.append("id")
                self.pila.append(",")
                self.pila.append("T")
            elif estado_actual == ",":
                self.coincidir(",")
                self.pila.append("id")
                self.pila.append(",")
                self.pila.append("T")
            elif estado_actual == "id":
                self.coincidir("id")
            elif estado_actual == "D":
                if self.token_actual.lower() == "distinct":
                    self.pila.append("P")
                    self.pila.append("distinct")
                else:
                    self.pila.append("P")  # D -> P
            elif estado_actual == "distinct":
                self.coincidir("distinct")
            elif estado_actual in ["*", "id"]:
                self.pila.append("A")
            elif estado_actual == "P":
                if self.token_actual == "*":
                    self.coincidir("*")
                elif self.token_actual.lower() == "id":
                    self.pila.append("A")
                else:
                    raise ValueError(f"Error de sintaxis. Se esperaba '*' o 'id' pero se encontró '{self.token_actual}'.")
            elif estado_actual == "A":
                if self.token_actual.lower() == "id":
                    self.pila.append("A1")
                    self.pila.append("A2")
                else:
                    raise ValueError(f"Error de sintaxis. Se esperaba 'id' pero se encontró '{self.token_actual}'.")
            elif estado_actual == "A1":
                if self.token_actual == ",":
                    self.coincidir(",")
                    self.pila.append("A")
                else:
                    pass  # A1 -> ε
            elif estado_actual == "A2":
                if self.token_actual == ".":
                    self.coincidir(".")
                    self.pila.append("id")
                else:
                    pass  # A2 -> ε
            elif estado_actual == "T":
                if self.token_actual.lower() == "id":
                    self.pila.append("T1")
                    self.pila.append("T2")
                else:
                    raise ValueError(f"Error de sintaxis. Se esperaba 'id' pero se encontró '{self.token_actual}'.")
            elif estado_actual == "T1":
                if self.token_actual == ",":
                    self.coincidir(",")
                    self.pila.append("T")
                else:
                    pass  # T1 -> ε
            elif estado_actual == "T2":
                if self.token_actual.lower() == "id":
                    self.pila.append("T3")
                else:
                    raise ValueError(f"Error de sintaxis. Se esperaba 'id' pero se encontró '{self.token_actual}'.")
            elif estado_actual == "T3":
                pass  # T3 -> ε
            else:
                raise ValueError(f"Error: Estado no reconocido en la pila: '{estado_actual}'.")

            print(f"Entrada: {self.tokens[self.indice:]}, Pila: {self.pila}")

def main():
    while True:
        consulta = input("Introduce una cadena SQL (o 'exit' para salir): ")

        if consulta.lower() == 'exit':
            break

        consulta += ' $'
        analizador = SQLParser(consulta)
        try:
            analizador.analizar()
        except Exception as e:
            print(f"Error al analizar la consulta: {e}")

if __name__ == "__main__":
    main()

