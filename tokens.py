class Token:
    """Конретный токен"""

    def __init__(self, token_type, text, lineno, pos):
        self.type = token_type
        self.text = text
        self.pos = pos
        self.lineno = lineno

    def __repr__(self):
        return f'<{self.type}, {self.text}, ({self.lineno}, {self.pos})>'


class TokenType:
    """ Класс определяющий тип токена и регулярное выражение по которому он находится"""

    def __init__(self, name, regex):
        self.name = name
        self.regex = regex

    def __repr__(self):
        return self.name


token_types = {
    "BOOLEAN-LITERAL": TokenType("BOOLEAN-LITERAL", "true|false"),
    "FLOAT-LITERAL": TokenType('FLOAT-LITERAL', '[+-]?([0-9]*[.]){1}[0-9]+'),
    "INT-LITERAL": TokenType('INT-LITERAL', '[0-9]*'),
    "STRING-LITERAL": TokenType('STRING-LITERAL', '".*?"'),

    "WHILE": TokenType('WHILE', "while"),
    "FOR": TokenType("FOR", "for"),

    "INT": TokenType("INT", "int"),
    "FLOAT": TokenType("FLOAT", "float"),
    "STRING": TokenType("STRING", "String"),
    "BOOLEAN": TokenType("BOOLEAN", "bool"),

    "IF": TokenType("IF", "if"),

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

    "PRINT": TokenType('PRINT', 'print'),

    "ID": TokenType('ID', '[A-Za-z][A-Za-z\\_\\-0-9]+'),

    "PLUS": TokenType('PLUS', '[+]'),
    "MINUS": TokenType('MINUS', '[-]'),
    "MULT": TokenType("MULTIPLE", "[*]"),
    "DIV": TokenType("DIV", "[/]"),

    "COMMENT": TokenType("COMMENT", "[#]"),

    "LBR": TokenType('LBR', '[(]'),
    "RBR": TokenType('RBR', '[)]'),
    "LBCR": TokenType("LBCR", "[{]"),
    "RBCR": TokenType("RBCR", '[}]')
}
