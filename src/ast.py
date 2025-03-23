class ASTNode:
    pass

class BinOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f'BinOp({self.left}, {self.op}, {self.right})'

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

class Variable(ASTNode):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'Variable({self.name})'

class PrintStatement(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'PrintStatement({self.value})'