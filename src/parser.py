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
    elif tokens[0][0] == 'IF':
        return parse_if_statement(tokens)
    elif tokens[0][0] == 'FOR':
        return parse_for_loop(tokens)
    elif tokens[0][0] == 'WHILE':
        return parse_while_loop(tokens)
    elif tokens[0][0] == 'FUNCTION':
        return parse_function_declaration(tokens)
    elif tokens[0][0] == 'RETURN':
        return parse_return_statement(tokens)
    else:
        return parse_expression(tokens)

def parse_if_statement(tokens):
    tokens.pop(0)  # Eliminar 'if'
    if tokens[0][0] != 'LPAREN':
        raise SyntaxError("Se esperaba '(' después de 'if'")
    tokens.pop(0)  # Eliminar '('
    condition = parse_expression(tokens)
    if tokens[0][0] != 'RPAREN':
        raise SyntaxError("Se esperaba ')' después de la condición")
    tokens.pop(0)  # Eliminar ')'
    if tokens[0][0] != 'LBRACE':
        raise SyntaxError("Se esperaba '{' después de 'if'")
    tokens.pop(0)  # Eliminar '{'
    body = parse_block(tokens)
    else_body = None
    if tokens and tokens[0][0] == 'ELSE':
        tokens.pop(0)  # Eliminar 'else'
        if tokens[0][0] != 'LBRACE':
            raise SyntaxError("Se esperaba '{' después de 'else'")
        tokens.pop(0)  # Eliminar '{'
        else_body = parse_block(tokens)
    return IfStatement(condition, body, else_body)

def parse_for_loop(tokens):
    tokens.pop(0)  # Eliminar 'for'
    if tokens[0][0] != 'LPAREN':
        raise SyntaxError("Se esperaba '(' después de 'for'")
    tokens.pop(0)  # Eliminar '('

    # Inicialización (puede ser una declaración de variable o una expresión)
    init = parse_var_declaration(tokens) if tokens[0][0] == 'VAR' else parse_expression(tokens)
    if tokens[0][0] != 'SEMICOLON':
        raise SyntaxError("Se esperaba ';' después de la inicialización")
    tokens.pop(0)  # Eliminar ';'

    # Condición
    condition = parse_expression(tokens)
    if tokens[0][0] != 'SEMICOLON':
        raise SyntaxError("Se esperaba ';' después de la condición")
    tokens.pop(0)  # Eliminar ';'

    # Actualización
    update = parse_expression(tokens)
    if tokens[0][0] != 'RPAREN':
        raise SyntaxError("Se esperaba ')' después de la actualización")
    tokens.pop(0)  # Eliminar ')'

    # Cuerpo del bucle
    if tokens[0][0] != 'LBRACE':
        raise SyntaxError("Se esperaba '{' después de 'for'")
    tokens.pop(0)  # Eliminar '{'
    body = parse_block(tokens)
    return ForLoop(init, condition, update, body)

def parse_while_loop(tokens):
    tokens.pop(0)  # Eliminar 'while'
    if tokens[0][0] != 'LPAREN':
        raise SyntaxError("Se esperaba '(' después de 'while'")
    tokens.pop(0)  # Eliminar '('
    condition = parse_expression(tokens)
    if tokens[0][0] != 'RPAREN':
        raise SyntaxError("Se esperaba ')' después de la condición")
    tokens.pop(0)  # Eliminar ')'
    if tokens[0][0] != 'LBRACE':
        raise SyntaxError("Se esperaba '{' después de 'while'")
    tokens.pop(0)  # Eliminar '{'
    body = parse_block(tokens)
    return WhileLoop(condition, body)

def parse_block(tokens):
    statements = []
    while tokens and tokens[0][0] != 'RBRACE':
        statements.append(parse_statement(tokens))
    if tokens and tokens[0][0] == 'RBRACE':
        tokens.pop(0)  # Eliminar '}'
    return statements

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

def parse_expression(tokens):
    return parse_assignment(tokens)

def parse_assignment(tokens):
    node = parse_logical_or(tokens)
    if tokens and tokens[0][0] == 'ASSIGN':
        op = tokens.pop(0)[1]
        value = parse_assignment(tokens)
        if isinstance(node, Variable):
            return VariableAssignment(node.name, value)
        else:
            raise SyntaxError("El lado izquierdo de una asignación debe ser una variable")
    return node

def parse_logical_or(tokens):
    node = parse_logical_and(tokens)
    while tokens and tokens[0][0] == 'OR':
        op = tokens.pop(0)[1]
        node = LogicalOp(node, op, parse_logical_and(tokens))
    return node

def parse_logical_and(tokens):
    node = parse_comparison(tokens)
    while tokens and tokens[0][0] == 'AND':
        op = tokens.pop(0)[1]
        node = LogicalOp(node, op, parse_comparison(tokens))
    return node

def parse_comparison(tokens):
    node = parse_add_sub(tokens)
    while tokens and tokens[0][0] in ('EQUAL', 'NOT_EQUAL', 'LESS', 'GREATER', 'LESS_EQUAL', 'GREATER_EQUAL'):
        op = tokens.pop(0)[1]
        node = ComparisonOp(node, op, parse_add_sub(tokens))
    return node

def parse_not(tokens):
    if tokens[0][0] == 'NOT':
        tokens.pop(0)  # Eliminar '!'
        return NotOp(parse_factor(tokens))
    return parse_factor(tokens)

def parse_function_declaration(tokens):
    tokens.pop(0)  # Eliminar 'function'
    name = tokens.pop(0)[1]  # Obtener el nombre de la función
    if tokens[0][0] != 'LPAREN':
        raise SyntaxError("Se esperaba '(' después del nombre de la función")
    tokens.pop(0)  # Eliminar '('
    parameters = []
    while tokens[0][0] != 'RPAREN':
        if tokens[0][0] == 'IDENTIFIER':
            parameters.append(tokens.pop(0)[1])  # Obtener el nombre del parámetro
        if tokens[0][0] == 'COMMA':
            tokens.pop(0)  # Eliminar ','
    tokens.pop(0)  # Eliminar ')'
    if tokens[0][0] != 'LBRACE':
        raise SyntaxError("Se esperaba '{' después de los parámetros")
    tokens.pop(0)  # Eliminar '{'
    body = parse_block(tokens)
    return FunctionDeclaration(name, parameters, body)

def parse_return_statement(tokens):
    tokens.pop(0)  # Eliminar 'return'
    value = parse_expression(tokens)
    # No es necesario verificar el punto y coma
    return ReturnStatement(value)

def parse_function_call(tokens, name):
    tokens.pop(0)  # Eliminar '('
    arguments = []
    while tokens[0][0] != 'RPAREN':
        arguments.append(parse_expression(tokens))
        if tokens[0][0] == 'COMMA':
            tokens.pop(0)  # Eliminar ','
    tokens.pop(0)  # Eliminar ')'
    return FunctionCall(name, arguments)

def parse_factor(tokens):
    if tokens[0][0] == 'VIDAS':
        return Number(int(tokens.pop(0)[1]))
    elif tokens[0][0] == 'PESO':
        return Float(float(tokens.pop(0)[1]))
    elif tokens[0][0] == 'COLA':
        return String(tokens.pop(0)[1][1:-1])  # Eliminar comillas
    elif tokens[0][0] == 'DORMIDO':
        value = tokens.pop(0)[1]
        return Boolean(value == 'true')
    elif tokens[0][0] == 'IDENTIFIER':
        name = tokens.pop(0)[1]
        if tokens and tokens[0][0] == 'LBRACKET':
            # Es un acceso a arreglo
            return parse_array_access(tokens, name)
        elif tokens and tokens[0][0] == 'LPAREN':
            # Es una llamada a función
            return parse_function_call(tokens, name)
        else:
            # Es una variable simple
            return Variable(name)
    elif tokens[0][0] == 'LPAREN':
        tokens.pop(0)  # Eliminar '('
        node = parse_expression(tokens)
        if tokens[0][0] != 'RPAREN':
            raise SyntaxError("Se esperaba ')' después de la expresión")
        tokens.pop(0)  # Eliminar ')'
        return node
    elif tokens[0][0] == 'LBRACKET':
        return parse_array(tokens)
    elif tokens[0][0] == 'NOT':
        return parse_not(tokens)
    else:
        raise SyntaxError(f'Token inesperado: {tokens[0][1]}')