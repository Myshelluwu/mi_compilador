import unittest
from src.lexer import lex
from src.parser import parse
from src.interpreter import Interpreter

class TestInterpreter(unittest.TestCase):
    def test_interpreter(self):
        code = "x = 10; y = x + 5;"
        tokens = lex(code)
        ast = parse(tokens)
        interpreter = Interpreter()
        interpreter.interpret(ast)
        self.assertEqual(interpreter.variables['x'], 10)
        self.assertEqual(interpreter.variables['y'], 15)

if __name__ == "__main__":
    unittest.main()