import re

TOKENS = [
    # Comentarios (deben estar al principio para que se ignoren primero)
    ('COMMENT_SINGLE', r'uwu.*'),  # Comentarios de una línea
    ('COMMENT_MULTIPLE', r'uwur[\s\S]*?uwur'),  # Comentarios de varias líneas

    # Palabras clave (deben estar antes de los identificadores)
    ('PRINT', r'meow'),  # Palabra clave 'print'
    ('VAR', r'michi'),  # Palabra clave 'var'
    ('IF', r'si'),  # Condicional if
    ('ELSE', r'entonces'),  # Condicional else
    ('FOR', r'cuando'),  # Bucle for
    ('WHILE', r'mientras'),  # Bucle while
    ('DORMIDO', r'true|false'),  # Booleanos
    ('FUNCTION', r'maullar'),  # Palabra clave 'function'
    ('RETURN', r'respuesta'),  # Palabra clave 'return'

    # Operadores y símbolos (deben estar antes de los identificadores y números)
    ('EQUAL', r'=='),  # Igualdad
    ('NOT_EQUAL', r'!='),  # Desigualdad
    ('LESS_EQUAL', r'<='),  # Menor o igual que
    ('GREATER_EQUAL', r'>='),  # Mayor o igual que
    ('LESS', r'<'),  # Menor que
    ('GREATER', r'>'),  # Mayor que
    ('AND', r'&&'),  # AND lógico
    ('OR', r'\|\|'),  # OR lógico
    ('NOT', r'!'),  # NOT lógico
    ('ASSIGN', r'='),  # Operador de asignación
    ('PLUS', r'\+'),  # Operador de suma
    ('MINUS', r'-'),  # Operador de resta
    ('MULTIPLY', r'\*'),  # Operador de multiplicación
    ('DIVIDE', r'/'),  # Operador de división

    # Símbolos y delimitadores
    ('DOT', r'\.'),  # Punto para acceso a métodos
    ('APPEND', r'agregar'),  # Método append
    ('POP', r'quitar'),  # Método pop
    ('LBRACE', r'\{'),  # Llave izquierda
    ('RBRACE', r'\}'),  # Llave derecha
    ('LPAREN', r'\('),  # Paréntesis izquierdo
    ('RPAREN', r'\)'),  # Paréntesis derecho
    ('LBRACKET', r'\['),  # Corchete izquierdo
    ('RBRACKET', r'\]'),  # Corchete derecho
    ('COMMA', r','),  # Coma
    ('COLON', r':'),  # Dos puntos
    ('SEMICOLON', r';'),  # Punto y coma

    # Literales (números, cadenas, identificadores)
    ('PESO', r'\d+\.\d+'),  # Números flotantes (debe estar antes de NUMBER)
    ('VIDAS', r'\d+'),  # Números enteros
    ('COLA', r'"[^"]*"'),  # Cadenas entre comillas dobles
    ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),  # Identificadores

    # Espacios en blanco y saltos de línea (deben estar al final)
    ('NEWLINE', r'\n'),  # Salto de línea
    ('WHITESPACE', r'\s+'),  # Espacios en blanco (ignorados)
]

def lex(code):
    tokens = []
    while code:
        for token_name, token_regex in TOKENS:
            match = re.match(token_regex, code)
            if match:
                value = match.group(0)
                # Ignorar comentarios y espacios en blanco
                if token_name not in ('COMMENT_SINGLE', 'COMMENT_MULTIPLE', 'WHITESPACE', 'NEWLINE'):
                    tokens.append((token_name, value))  # Asegúrate de que sea una tupla (tipo, valor)
                code = code[len(value):]
                break
        else:
            # Imprime el carácter inesperado y el contexto
            print(f"Carácter inesperado: '{code[0]}' en el contexto: '{code[:10]}'")
            print(f"Código restante: '{code}'")
            raise SyntaxError(f'Token inesperado: {code[0]}')
    return tokens