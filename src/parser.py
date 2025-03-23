from src.ast import *

def parse(tokens):
    statements = []
    while tokens:
        # Ignorar saltos de línea al inicio
        while tokens and tokens[0][0] == 'NEWLINE':
            tokens.pop(0)
        if not tokens:
            break
        statement = parse_statement(tokens)
        statements.append(statement)
    return statements

def parse_statement(tokens):
    if tokens[0][0] == 'VAR':
        return parse_var_declaration(tokens)
    elif tokens[0][0] == 'PRINT':
        return parse_print_statement(tokens)
    else:
        return parse_expression(tokens)

def parse_var_declaration(tokens):
    tokens.pop(0)  # Eliminar 'var'
    name = tokens.pop(0)[1]  # Obtener el nombre de la variable
    tokens.pop(0)  # Eliminar '='
    value = parse_expression(tokens)  # Obtener el valor de la variable
    # Ignorar saltos de línea al final
    while tokens and tokens[0][0] == 'NEWLINE':
        tokens.pop(0)
    return VariableDeclaration(name, value)

def parse_print_statement(tokens):
    tokens.pop(0)  # Eliminar 'print'
    if tokens[0][0] != 'LPAREN':
        raise SyntaxError("Se esperaba '(' después de 'print'")
    tokens.pop(0)  # Eliminar '('
    value = parse_expression(tokens)  # Obtener el valor a imprimir
    if tokens[0][0] != 'RPAREN':
        raise SyntaxError("Se esperaba ')' después de la expresión")
    tokens.pop(0)  # Eliminar ')'
    # Ignorar saltos de línea al final
    while tokens and tokens[0][0] == 'NEWLINE':
        tokens.pop(0)
    return PrintStatement(value)

def parse_expression(tokens):
    if tokens[0][0] == 'LBRACKET':
        return parse_array(tokens)
    else:
        return parse_add_sub(tokens)

def parse_array(tokens):
    tokens.pop(0)  # Eliminar '['
    elements = []
    while tokens[0][0] != 'RBRACKET':
        elements.append(parse_expression(tokens))
        if tokens[0][0] == 'COMMA':
            tokens.pop(0)  # Eliminar ','
    tokens.pop(0)  # Eliminar ']'
    return Array(elements)


def parse_add_sub(tokens):
    node = parse_mul_div(tokens)
    while tokens and tokens[0][0] in ('PLUS', 'MINUS'):
        op = tokens.pop(0)[1]
        node = BinOp(node, op, parse_mul_div(tokens))
    return node

def parse_mul_div(tokens):
    node = parse_factor(tokens)
    while tokens and tokens[0][0] in ('MULTIPLY', 'DIVIDE'):
        op = tokens.pop(0)[1]
        node = BinOp(node, op, parse_factor(tokens))
    return node

def parse_factor(tokens):
    if tokens[0][0] == 'NUMBER':
        return Number(int(tokens.pop(0)[1]))
    elif tokens[0][0] == 'STRING':
        return String(tokens.pop(0)[1])  # Crear un nodo String
    elif tokens[0][0] == 'IDENTIFIER':
        name = tokens.pop(0)[1]
        if tokens and tokens[0][0] == 'LBRACKET':
            return parse_array_access(tokens, name)
        return Variable(name)
    elif tokens[0][0] == 'LPAREN':
        tokens.pop(0)  # Eliminar '('
        node = parse_expression(tokens)
        if tokens[0][0] != 'RPAREN':
            raise SyntaxError("Se esperaba ')' después de la expresión")
        tokens.pop(0)  # Eliminar ')'
        return node
    elif tokens[0][0] == 'LBRACKET':
        return parse_array(tokens)  # Manejar arreglos directamente
    else:
        raise SyntaxError(f'Token inesperado: {tokens[0][1]}')

def parse_array_access(tokens, name):
    indices = []
    while tokens and tokens[0][0] == 'LBRACKET':
        tokens.pop(0)  # Eliminar '['
        index = parse_expression(tokens)
        indices.append(index)
        if tokens[0][0] != 'RBRACKET':
            raise SyntaxError("Se esperaba ']' después del índice")
        tokens.pop(0)  # Eliminar ']'
    return ArrayAccess(name, indices)