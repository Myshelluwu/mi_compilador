class CompilerError(Exception):
    pass

class SyntaxError(CompilerError):
    pass

class SemanticError(CompilerError):
    pass