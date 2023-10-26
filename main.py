from lexer import Lexer
from parser import Parser
from abs_st import print_ast
from generator import CodeGenerator
from semantic import SemanticAnalyzer


if __name__ == '__main__':
    code = open('functions_code.dart', 'r').read()

    lexer = Lexer(code)
    lexer.analyze()
    parser = Parser([i for i in lexer.tokens])
    root = parser.parseFile()

    print_ast(root)

    semantic = SemanticAnalyzer(root)
    semantic.analyze()
    #
    generator = CodeGenerator(root)
    generator.generate()
    generator.write_generated_code('123')


