from .ast import *  # Importa todas las clases del AST

class Interpreter:
    def __init__(self):
        self.michis = {}  # Diccionario para almacenar variables
        self.functions = {}  # Diccionario para almacenar funciones

    def interpret(self, statements):    
        """
        Ejecuta una lista de declaraciones (statements).
        """
        for statement in statements:
            if isinstance(statement, MichiDeclaration):
                # Declaración de variable: guarda el valor en el diccionario
                self.michis[statement.name] = self.evaluate(statement.value)
            elif isinstance(statement, MeowStatement):
                # Declaración de impresión: evalúa y muestra el valor
                value = self.evaluate(statement.value)
                print(value)
            elif isinstance(statement, IfStatement):
                # Condicional if
                condition = self.evaluate(statement.condition)
                if condition:
                    self.interpret(statement.body)
                elif statement.else_body:
                    self.interpret(statement.else_body)
            elif isinstance(statement, ForLoop):
                # Bucle for
                self.evaluate(statement.init)  # Ejecuta la inicialización (puede ser una declaración de variable)
                while self.evaluate(statement.condition):  # Evalúa la condición
                    self.interpret(statement.body)  # Ejecuta el cuerpo del bucle
                    self.evaluate(statement.update)  # Ejecuta la actualización
            elif isinstance(statement, WhileLoop):
                # Bucle while
                while self.evaluate(statement.condition):  # Evalúa la condición
                    self.interpret(statement.body)  # Ejecuta el cuerpo del bucle
            elif isinstance(statement, FunctionDeclaration):
                self.functions[statement.name] = statement  # Guardar la función
            elif isinstance(statement, ReturnStatement):
                return self.evaluate(statement.value)  # Retornar el valor
            else:
                # Otras declaraciones (expresiones)
                self.evaluate(statement)

    def evaluate(self, node):
        if isinstance(node, Vidas):
            return node.value
        elif isinstance(node, Peso):
            return node.value
        elif isinstance(node, Cola):
            return node.value
        elif isinstance(node, Dormido):
            return node.value
        elif isinstance(node, Array):
            return [self.evaluate(element) for element in node.elements]
        elif isinstance(node, ArrayAccess):
            array = self.michis.get(node.name)
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
        elif isinstance(node, ComparisonOp):
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)
            if node.op == '==':
                return left == right
            elif node.op == '!=':
                return left != right
            elif node.op == '<':
                return left < right
            elif node.op == '>':
                return left > right
            elif node.op == '<=':
                return left <= right
            elif node.op == '>=':
                return left >= right
        elif isinstance(node, LogicalOp):
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)
            if node.op == '&&':
                return left and right
            elif node.op == '||':
                return left or right
        elif isinstance(node, MichiAssignment):
            self.michis[node.name] = self.evaluate(node.value)
            return self.michis[node.name]
        elif isinstance(node, MichiDeclaration):
            self.michis[node.name] = self.evaluate(node.value)
            return self.michis[node.name]
        elif isinstance(node, NotOp):
            return not self.evaluate(node.expr)
        elif isinstance(node, Michi):
            return self.michis.get(node.name, 0)
        elif isinstance(node, Michi):
            # Nodo Variable: devuelve el valor de la variable
            return self.michis.get(node.name, 0)
        elif isinstance(node, FunctionCall):
            function = self.functions.get(node.name)
            if function is None:
                raise ValueError(f'Función no definida: {node.name}')
            # Crear un nuevo ámbito para los parámetros
            old_michis = self.michis.copy()
            for param_name, arg_value in zip(function.parameters, node.arguments):
                self.michis[param_name] = self.evaluate(arg_value)
            # Ejecutar el cuerpo de la función
            result = None
            for statement in function.body:
                result = self.interpret([statement])
                if isinstance(statement, ReturnStatement):
                    break
            # Restaurar el ámbito anterior
            self.michis = old_michis
            return result
        else:
            # Si el nodo no es reconocido, lanza un error
            raise ValueError(f'Nodo AST no reconocido: {node}')