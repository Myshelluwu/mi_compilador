from .ast import *
def generate_code(node):
    if isinstance(node, Number):
        return str(node.value)
    elif isinstance(node, BinOp):
        left = generate_code(node.left)
        right = generate_code(node.right)
        return f'({left} {node.op} {right})'
    elif isinstance(node, Variable):
        return node.name
    elif isinstance(node, VariableAssignment):
        return f'{node.name} = {generate_code(node.value)}'
    else:
        raise ValueError(f'Nodo AST no reconocido: {node}')