from .ast import *  # Importa todas las clases del AST

class Interpreter:
    def __init__(self):
        self.variables = {}  # Diccionario para almacenar variables
        self.functions = {}  # Diccionario para almacenar funciones

    def interpret(self, statements):    
        """
        Ejecuta una lista de declaraciones (statements).
        """
        for statement in statements:
            if isinstance(statement, VariableDeclaration):
                # Declaración de variable: guarda el valor en el diccionario
                self.variables[statement.name] = self.evaluate(statement.value)
            elif isinstance(statement, PrintStatement):
                # Declaración de impresión: evalúa y muestra los valores
                values = [self.evaluate(arg) for arg in statement.arguments]
                print(*values)  # Desempaquetar los valores para print
            elif isinstance(statement, IfStatement):
                # Condicional if
                condition = self.evaluate(statement.condition)
                if condition:
                    result = self.interpret(statement.body)
                    if result is not None:
                        return result
                elif statement.else_body:
                    result = self.interpret(statement.else_body)
                    if result is not None:
                        return result
            elif isinstance(statement, ForLoop):
                # Bucle for
                self.evaluate(statement.init)  # Ejecuta la inicialización (puede ser una declaración de variable)
                while self.evaluate(statement.condition):  # Evalúa la condición
                    result = self.interpret(statement.body)  # Ejecuta el cuerpo del bucle
                    if result is not None:
                        return result
                    self.evaluate(statement.update)  # Ejecuta la actualización
            elif isinstance(statement, WhileLoop):
                # Bucle while
                while self.evaluate(statement.condition):  # Evalúa la condición
                    result = self.interpret(statement.body)  # Ejecuta el cuerpo del bucle
                    if result is not None:
                        return result
            elif isinstance(statement, FunctionDeclaration):
                self.functions[statement.name] = statement  # Guardar la función
            elif isinstance(statement, ReturnStatement):
                return self.evaluate(statement.value)  # Retornar el valor
            else:
                # Otras declaraciones (expresiones)
                result = self.evaluate(statement)
                if isinstance(statement, FunctionCall):
                    # Solo imprimir si no es parte de una asignación y el resultado no es None
                    if not statement.is_assignment and result is not None:
                        print(result)
                    return result

    def evaluate(self, node):
        if isinstance(node, Number):
            return node.value
        elif isinstance(node, Float):
            return node.value
        elif isinstance(node, String):
            return node.value
        elif isinstance(node, Boolean):
            return node.value
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
                # Convertir índice negativo a positivo
                if index < 0:
                    index = len(array) + index
                if index < 0 or index >= len(array):
                    raise ValueError(f'Índice fuera de rango: {index}')
                array = array[index]
            return array
        elif isinstance(node, MethodCall):
            obj = self.variables.get(node.object_name)
            if obj is None:
                raise ValueError(f'Objeto no definido: {node.object_name}')
            
            if node.method_name == 'agregar':
                if not isinstance(obj, list):
                    raise ValueError(f'El método agregar solo puede ser usado en arrays')
                if len(node.arguments) != 1:
                    raise ValueError(f'El método agregar requiere exactamente un argumento')
                value = self.evaluate(node.arguments[0])
                obj.append(value)
                return obj
            elif node.method_name == 'quitar':
                if not isinstance(obj, list):
                    raise ValueError(f'El método quitar solo puede ser usado en arrays')
                if len(node.arguments) > 1:
                    raise ValueError(f'El método quitar acepta máximo un argumento')
                if len(node.arguments) == 1:
                    # Si se proporciona un índice
                    index = self.evaluate(node.arguments[0])
                    if not isinstance(index, int):
                        raise ValueError(f'El índice debe ser un número entero')
                    if index < 0 or index >= len(obj):
                        raise ValueError(f'Índice fuera de rango: {index}')
                    return obj.pop(index)
                else:
                    # Si no se proporciona índice, quita el último elemento
                    if not obj:
                        raise ValueError('No se puede quitar elementos de un array vacío')
                    return obj.pop()
            else:
                raise ValueError(f'Método no reconocido: {node.method_name}')
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
        elif isinstance(node, VariableAssignment):
            self.variables[node.name] = self.evaluate(node.value)
            return self.variables[node.name]
        elif isinstance(node, VariableDeclaration):
            self.variables[node.name] = self.evaluate(node.value)
            return self.variables[node.name]
        elif isinstance(node, NotOp):
            return not self.evaluate(node.expr)
        elif isinstance(node, Variable):
            return self.variables.get(node.name, 0)
        elif isinstance(node, Variable):
            # Nodo Variable: devuelve el valor de la variable
            return self.variables.get(node.name, 0)
        elif isinstance(node, FunctionCall):
            function = self.functions.get(node.name)
            if function is None:
                raise ValueError(f'Función no definida: {node.name}')
            # Crear un nuevo ámbito para los parámetros
            old_variables = self.variables.copy()
            for param_name, arg_value in zip(function.parameters, node.arguments):
                self.variables[param_name] = self.evaluate(arg_value)
            # Ejecutar el cuerpo de la función
            result = None
            for statement in function.body:
                result = self.interpret([statement])
                if isinstance(statement, ReturnStatement):
                    break
            # Restaurar el ámbito anterior
            self.variables = old_variables
            return result
        elif isinstance(node, LenFunction):
            value = self.evaluate(node.value)
            if isinstance(value, list):
                return len(value)
            elif isinstance(value, str):
                return len(value)
            else:
                raise ValueError(f'No se puede obtener la longitud de {type(value)}')
        else:
            # Si el nodo no es reconocido, lanza un error
            raise ValueError(f'Nodo AST no reconocido: {node}')