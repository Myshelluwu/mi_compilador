import unittest
from src.lexer import lex
from src.parser import parse

class TestParser(unittest.TestCase):
    def test_parser(self):
        code = "x = 10;"
        tokens = lex(code)
        ast = parse(tokens)
        self.assertEqual(len(ast), 1)
        self.assertEqual(ast[0].name, 'x')
        self.assertEqual(ast[0].value.value, 10)

if __name__ == "__main__":
    unittest.main()