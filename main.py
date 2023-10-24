from lexer import Lexer
from parser import Parser
from ast import print_ast


if __name__ == '__main__':
    code = open('code.dart', 'r').read()

    lexer = Lexer(code)
    lexer.analyze()

    parser = Parser([i for i in lexer.tokens])
    root = parser.parseCode()
    print_ast(root)

    parser.run(root)




