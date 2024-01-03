from lexer import Lexer
from parser import Parser
from abs_st import print_ast
from generator import CodeGenerator
from semantic import SemanticAnalyzer
import subprocess

def apply_prettier_to_file(file_path):
    try:
        print("[+] Trying to start Prettier")
        subprocess.run(["npx", "prettier", "--write", file_path], check=True)
        print(f"[+] Prettier applied successfully to {file_path}")
    except subprocess.CalledProcessError as e:
        print(f"[-] An error occurred while applying Prettier: {e}")


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

    apply_prettier_to_file('result.js')

