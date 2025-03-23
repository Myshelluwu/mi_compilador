from src.lexer import lex

code = """
var a = 10

if (a > 5) {
    print("a es mayor que 5")
} else {
    print("a es menor o igual que 5")
}

for (var i = 0; i < 3; i = i + 1) {
    print(i)
}

var j = 0
while (j < 3) {
    print(j)
    j = j + 1
}

"""

tokens = lex(code)
for token in tokens:
    print(token)