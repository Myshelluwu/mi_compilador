import re

TOKENS = [
    ('COMMENT_SINGLE', r'#.*'),  # Comentarios de una línea
    ('COMMENT_MULTIPLE', r'/\*.*?\*/'),  # Comentarios de varias líneas
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
                # Ignorar comentarios y espacios en blanco
                if token_name not in ('COMMENT_SINGLE', 'COMMENT_MULTI', 'WHITESPACE'):
                    tokens.append((token_name, value))  # Asegúrate de que sea una tupla (tipo, valor)
                code = code[len(value):]
                break
        else:
            raise SyntaxError(f'Carácter inesperado: {code[0]}')
    return tokens