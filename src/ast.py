class ASTNode:
    pass

class BinOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f'BinOp({self.left}, {self.op}, {self.right})'

# Operaciones lógicas
class LogicalOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f'LogicalOp({self.left}, {self.op}, {self.right})'

# Comparaciones
class ComparisonOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f'ComparisonOp({self.left}, {self.op}, {self.right})'

# NOT lógico
class NotOp(ASTNode):
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return f'NotOp({self.expr})'

class Number(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'Number({self.value})'

class Float(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'Float({self.value})'

class String(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'String({self.value})'

class Boolean(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'Boolean({self.value})'
    
# Condicional if
class IfStatement(ASTNode):
    def __init__(self, condition, body, else_body=None):
        self.condition = condition
        self.body = body
        self.else_body = else_body

    def __repr__(self):
        return f'IfStatement({self.condition}, {self.body}, else={self.else_body})'

# Bucle for
class ForLoop(ASTNode):
    def __init__(self, init, condition, update, body):
        self.init = init
        self.condition = condition
        self.update = update
        self.body = body

    def __repr__(self):
        return f'ForLoop({self.init}, {self.condition}, {self.update}, {self.body})'

# Bucle while
class WhileLoop(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f'WhileLoop({self.condition}, {self.body})'

class Array(ASTNode):
    def __init__(self, elements):
        self.elements = elements

    def __repr__(self):
        return f'Array({self.elements})'

class ArrayAccess(ASTNode):
    def __init__(self, name, indices):
        self.name = name
        self.indices = indices

    def __repr__(self):
        return f'ArrayAccess({self.name}, {self.indices})'

class VariableDeclaration(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return f'VariableDeclaration({self.name}, {self.value})'
    
class VariableAssignment(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return f'VariableAssignment({self.name}, {self.value})'

class Variable(ASTNode):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'Variable({self.name})'

class PrintStatement(ASTNode):
    def __init__(self, arguments):
        self.arguments = arguments  # Lista de argumentos a imprimir

    def __repr__(self):
        return f'PrintStatement({self.arguments})'
    
class FunctionDeclaration(ASTNode):
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters  # Lista de nombres de parámetros
        self.body = body  # Lista de declaraciones en el cuerpo de la función

    def __repr__(self):
        return f'FunctionDeclaration({self.name}, {self.parameters}, {self.body})'

class FunctionCall(ASTNode):
    def __init__(self, name, arguments, is_assignment=False):
        self.name = name
        self.arguments = arguments  # Lista de argumentos
        self.is_assignment = is_assignment  # Indica si es parte de una asignación

    def __repr__(self):
        return f'FunctionCall({self.name}, {self.arguments}, is_assignment={self.is_assignment})'

class MethodCall(ASTNode):
    def __init__(self, object_name, method_name, arguments):
        self.object_name = object_name
        self.method_name = method_name
        self.arguments = arguments

    def __repr__(self):
        return f'MethodCall({self.object_name}.{self.method_name}, {self.arguments})'

class ReturnStatement(ASTNode):
    def __init__(self, value):
        self.value = value  # Valor a retornar

    def __repr__(self):
        return f'ReturnStatement({self.value})'

class LenFunction(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'LenFunction({self.value})'