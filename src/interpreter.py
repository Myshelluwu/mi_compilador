from .ast import *  # Importa todas las clases del AST

class Interpreter:
    def __init__(self):
        self.variables = {}  # Diccionario para almacenar variables

    def interpret(self, statements):
        """
        Ejecuta una lista de declaraciones (statements).
        """
        for statement in statements:
            if isinstance(statement, VariableDeclaration):
                # Declaración de variable: guarda el valor en el diccionario
                self.variables[statement.name] = self.evaluate(statement.value)
            elif isinstance(statement, PrintStatement):
                # Declaración de impresión: evalúa y muestra el valor
                value = self.evaluate(statement.value)
                print(value)
            else:
                # Otras declaraciones (expresiones)
                self.evaluate(statement)

    def evaluate(self, node):
        """
        Evalúa un nodo del AST y devuelve su valor.
        """
        if isinstance(node, Number):
            # Nodo Number: devuelve el valor entero
            return node.value
        elif isinstance(node, Float):
            # Nodo Float: devuelve el valor flotante
            return node.value
        elif isinstance(node, String):
            # Nodo String: devuelve el valor de la cadena
            return node.value
        elif isinstance(node, Boolean):
            # Nodo Boolean: devuelve el valor booleano
            return node.value
        elif isinstance(node, Array):
            # Nodo Array: evalúa cada elemento y devuelve una lista
            return [self.evaluate(element) for element in node.elements]
        elif isinstance(node, ArrayAccess):
            # Nodo ArrayAccess: accede a un elemento del arreglo
            array = self.variables.get(node.name)
            if array is None:
                raise ValueError(f'Arreglo no definido: {node.name}')
            indices = [self.evaluate(index) for index in node.indices]
            for index in indices:
                if not isinstance(index, int):
                    raise ValueError(f'Índice no válido: {index}')
                if index < 0 or index >= len(array):
                    raise ValueError(f'Índice fuera de rango: {index}')
                array = array[index]
            return array
        elif isinstance(node, BinOp):
            # Nodo BinOp: evalúa operaciones binarias (+, -, *, /)
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)
            if node.op == '+':
                return left + right
            elif node.op == '-':
                return left - right
            elif node.op == '*':
                return left * right
            elif node.op == '/':
                return left / right
        elif isinstance(node, Variable):
            # Nodo Variable: devuelve el valor de la variable
            return self.variables.get(node.name, 0)
        else:
            # Si el nodo no es reconocido, lanza un error
            raise ValueError(f'Nodo AST no reconocido: {node}')