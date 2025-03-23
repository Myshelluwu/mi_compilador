from src.lexer import lex
from src.parser import parse
from src.interpreter import Interpreter

def leer_archivo(ruta):
    """
    Lee el contenido de un archivo y lo devuelve como una cadena.
    """
    with open(ruta, 'r') as archivo:
        return archivo.read()

def main():
    print("Interpretador de Kiki")
    ruta_archivo = "examples/"+input("Ingrese el nombre del archivo .kiki: ")+".kiki"
    # Especifica la ruta del archivo .kiki
    try:
        # Lee el contenido del archivo .kiki
        codigo = leer_archivo(ruta_archivo)

        # Procesa el código
        tokens = lex(codigo)
        ast = parse(tokens)
        interpreter = Interpreter()
        interpreter.interpret(ast)

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {ruta_archivo}")
    except Exception as e:
        print(f"Error durante la ejecución: {e}")

if __name__ == "__main__":
    main()