from lexer import Lexer
from parser import Parser
from abs_st import print_ast
from generator import CodeGenerator
from semantic import SemanticAnalyzer
from prettyfi import apply_prettier_to_file


if __name__ == '__main__':
    code = open('examples/example.dart', 'r').read()

    lexer = Lexer(code)
    lexer.analyze()

    # Вывод комментариев
    print("Комментарии")
    print(lexer.comments)
    print("")


    parser = Parser([i for i in lexer.tokens])
    root = parser.parseFile()

    print_ast(root)

    semantic = SemanticAnalyzer(root)
    semantic.analyze()

    generator = CodeGenerator(root)
    generator.generate()
    generator.write_generated_code('result.js')

    apply_prettier_to_file('result.js') # не обязательно; нужен node, npx и глобально установленный prettier

