class Token:
    """Конретный токен"""

    def __init__(self, token_type, text, lineno, pos):
        self.type = token_type
        self.text = text
        self.pos = pos
        self.lineno = lineno

    def __repr__(self):
        return f'<{self.type}, {self.text}, ({self.lineno}, {self.pos})>'

    def get_pos(self):
        return self.lineno, self.pos

class TokenType:
    """ Класс определяющий тип токена и регулярное выражение по которому он находится"""

    def __init__(self, name, regex):
        self.name = name
        self.regex = regex

    def __repr__(self):
        return self.name


token_types = {
    "BOOLEAN-LITERAL": TokenType("BOOLEAN-LITERAL", "true|false"),
    "COMMA": TokenType("COMMA", "[,]"),
    "FLOAT-LITERAL": TokenType('FLOAT-LITERAL', '[+-]?([0-9]*[.]){1}[0-9]+'),
    "INT-LITERAL": TokenType('INT-LITERAL', '[0-9]*'),
    "STRING-LITERAL": TokenType('STRING-LITERAL', '".*?"'),

    "WHILE": TokenType('WHILE', "while"),
    "FOR": TokenType("FOR", "for"),

    "FUNDEC": TokenType("FUNDEC", "decl"),

    "IF": TokenType("IF", "if"),
    "ELSE": TokenType("ELSE", "else"),

    "SEMICOLON": TokenType('SEMICOLON', ';'),

    "SPACE": TokenType('SPACE', '[ \\t\\r]'),
    "NEXTLINE": TokenType('NEXTLINE', "\\n"),

    "OR": TokenType("OR", "[|][|]"),
    "AND": TokenType("AND", "&&"),

    "NE": TokenType("NE", "!="),
    "E": TokenType("EQUAL", "=="),
    "LE": TokenType("LE", "<="),
    "GE": TokenType("GE", ">="),
    "NOT": TokenType("NOT", "[!]"),
    "L": TokenType("L", "[<]"),
    "G": TokenType("G", "[>]"),

    "ASSIGN": TokenType('ASSIGN', '[=]'),

    "ID": TokenType('ID', '[A-Za-z][A-Za-z\\_\\-0-9]*'),

    "PLUS": TokenType('PLUS', '[+]'),
    "MINUS": TokenType('MINUS', '[-]'),
    "MULT": TokenType("MULT", "[*]"),
    "INLINE-COMMENT": TokenType("INLINE-COMMENT", "^//.*\n"),
    "DIV": TokenType("DIV", "[/]"),

    "LBR": TokenType('LBR', '[(]'),
    "RBR": TokenType('RBR', '[)]'),
    "LBCR": TokenType("LBCR", "[\\{]"),
    "RBCR": TokenType("RBCR", '[}]')
}
