import unittest
from src.lexer import lex

class TestLexer(unittest.TestCase):
    def test_lexer(self):
        code = "x = 10;"
        tokens = lex(code)
        self.assertEqual(tokens, [('IDENTIFIER', 'x'), ('ASSIGN', '='), ('NUMBER', '10'), ('SEMICOLON', ';')])

if __name__ == "__main__":
    unittest.main()