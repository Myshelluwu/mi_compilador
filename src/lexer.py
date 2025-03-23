import re

TOKENS = [
    ('PRINT', r'print'),  # Palabra clave 'print'
    ('VAR', r'var'),  # Palabra clave 'var'
    ('NUMBER', r'\d+'),  # Números enteros
    ('STRING', r"'[^']*'"),  # Cadenas entre comillas simples
    ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),  # Identificadores
    ('ASSIGN', r'='),  # Operador de asignación
    ('PLUS', r'\+'),  # Operador de suma
    ('MINUS', r'-'),  # Operador de resta
    ('MULTIPLY', r'\*'),  # Operador de multiplicación
    ('DIVIDE', r'/'),  # Operador de división
    ('LPAREN', r'\('),  # Paréntesis izquierdo
    ('RPAREN', r'\)'),  # Paréntesis derecho
    ('LBRACKET', r'\['),  # Corchete izquierdo
    ('RBRACKET', r'\]'),  # Corchete derecho
    ('COMMA', r','),  # Coma
    ('NEWLINE', r'\n'),  # Salto de línea
    ('WHITESPACE', r'\s+'),  # Espacios en blanco
]

def lex(code):
    tokens = []
    while code:
        for token_name, token_regex in TOKENS:
            match = re.match(token_regex, code)
            if match:
                value = match.group(0)
                if token_name != 'WHITESPACE':  # Ignorar espacios en blanco
                    tokens.append((token_name, value))
                code = code[len(value):]
                break
        else:
            raise SyntaxError(f'Carácter inesperado: {code[0]}')
    return tokens