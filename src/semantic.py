from .ast import *
from .errors import SemanticError

class SemanticAnalyzer:
    def __init__(self):
        self.variables = set()

    def analyze(self, node):
        if isinstance(node, VariableDeclaration):
            if node.name in self.variables:
                raise SemanticError(f'Variable ya declarada: {node.name}')
            self.variables.add(node.name)
        elif isinstance(node, VariableAssignment):
            if node.name not in self.variables:
                raise SemanticError(f'Variable no declarada: {node.name}')