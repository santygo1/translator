from lexer import Lexer
from parser import Parser
from abs_st import print_ast


if __name__ == '__main__':
    code = open('examples/example.dart', 'r').read()

    lexer = Lexer(code)
    lexer.analyze()
    parser = Parser([i for i in lexer.tokens])
    root = parser.parseFile()

    print_ast(root)




