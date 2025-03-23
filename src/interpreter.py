from .ast import *

class Interpreter:
    def __init__(self):
        self.variables = {}

    def interpret(self, statements):
        for statement in statements:
            if isinstance(statement, VariableDeclaration):
                self.variables[statement.name] = self.evaluate(statement.value)
            elif isinstance(statement, PrintStatement):
                value = self.evaluate(statement.value)
                print(value)  # Imprimir el valor
            else:
                self.evaluate(statement)

    def evaluate(self, node):
        if isinstance(node, Number):
            return node.value
        elif isinstance(node, String):
            return node.value  # Devolver el valor de la cadena
        elif isinstance(node, Array):
            return [self.evaluate(element) for element in node.elements]
        elif isinstance(node, ArrayAccess):
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
            return self.variables.get(node.name, 0)
        else:
            raise ValueError(f'Nodo AST no reconocido: {node}')