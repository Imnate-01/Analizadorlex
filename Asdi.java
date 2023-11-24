import java.util.Stack;

public class AnalizadorSintactico {

    public static boolean analizarEntrada(String entrada) {
        Stack<String> pila = new Stack<>();
        pila.push("$");
        pila.push("Q");

        int indiceEntrada = 0;

        while (!pila.isEmpty()) {
            String simboloPila = pila.pop();

            if (!esTerminal(simboloPila)) {
                if (simboloPila.equals("Q")) {
                    if (entrada.startsWith("select")) {
                        pila.push("$");
                        pila.push("from");
                        pila.push("T");
                        pila.push("D");
                        pila.push("select");
                    } else {
                        System.out.println("Error: Se esperaba 'select'");
                        return false;
                    }
                } else if (simboloPila.equals("D")) {
                    if (entrada.startsWith("distinct")) {
                        pila.push("P");
                        pila.push("distinct");
                    } else {
                        pila.push("P");
                    }
                } else if (simboloPila.equals("P")) {
                    if (entrada.startsWith("*")) {
                        pila.push("*");
                    } else {
                        pila.push("A");
                    }
                } else if (simboloPila.equals("A")) {
                    pila.push("A1");
                    pila.push("A2");
                } else if (simboloPila.equals("A1")) {
                    if (entrada.startsWith(",")) {
                        pila.push("A");
                        pila.push(",");
                    } else {
                        pila.push(epsilon());
                    }
                } else if (simboloPila.equals("A2")) {
                    if (entrada.startsWith("id")) {
                        pila.push("A3");
                        pila.push("id");
                    } else {
                        System.out.println("Error: Se esperaba 'id'");
                        return false;
                    }
                } else if (simboloPila.equals("A3")) {
                    if (entrada.startsWith(".")) {
                        pila.push("id");
                        pila.push(".");
                    } else {
                        pila.push(epsilon());
                    }
                } else if (simboloPila.equals("T")) {
                    pila.push("T1");
                    pila.push("T2");
                } else if (simboloPila.equals("T1")) {
                    if (entrada.startsWith(",")) {
                        pila.push("T");
                        pila.push(",");
                    } else {
                        pila.push(epsilon());
                    }
                } else if (simboloPila.equals("T2")) {
                    if (entrada.startsWith("id")) {
                        pila.push("T3");
                        pila.push("id");
                    } else {
                        System.out.println("Error: Se esperaba 'id'");
                        return false;
                    }
                } else if (simboloPila.equals("T3")) {
                    pila.push("id");
                }
                // ... continuar con otras producciones según la gramática
            } else {
                String simboloActual = obtenerTerminal(entrada, indiceEntrada);
                if (simboloPila.equals(simboloActual)) {
                    indiceEntrada++;
                } else {
                    System.out.println("Error: Se esperaba '" + simboloPila + "', pero se encontró '" + simboloActual + "'");
                    return false;
                }
            }
        }

        if (indiceEntrada == entrada.length()) {
            System.out.println("La entrada es válida.");
            return true;
        } else {
            System.out.println("Error: La entrada contiene símbolos adicionales no esperados.");
            return false;
        }
    }

    private static boolean esTerminal(String simbolo) {
        return simbolo.equals("select") || simbolo.equals("distinct") || simbolo.equals("*")
                || simbolo.equals(",") || simbolo.equals(".") || simbolo.equals("id");
    }

    private static String obtenerTerminal(String entrada, int indice) {
        return Character.toString(entrada.charAt(indice));
    }

    private static String epsilon() {
        return "Ɛ";
    }

    public static void main(String[] args) {
        String entrada = "select id from id";
        analizarEntrada(entrada);
    }
}
