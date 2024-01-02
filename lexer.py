from tokens import Token, token_types
from comment import Comment
import re as matcher


class Lexer:

    def __init__(self, code):
        self.code = code
        self.pos = 0  # Позиция элемента
        self.linepos = [1, 1]  # Точная позиция в тексте
        self.tokens = []
        self.comments = []

    def analyze(self):
        while self.next_token():
            pass

        self.__delete_tokens("SPACE")
        self.__delete_tokens("NEXTLINE")

        return self.tokens

    def __delete_tokens(self, token_type_name):
        self.tokens = filter(lambda token: token.type.name != token_types[token_type_name].name, self.tokens)

    def next_token(self):
        if self.pos >= len(self.code):
            return False

        token_types_values = token_types.values()
        for token_type in token_types_values:

            regex = '^' + token_type.regex
            result = matcher.match(regex, self.code[self.pos:])

            if result and result[0]:
                token = Token(token_type, result[0], self.linepos[0], self.linepos[1])

                # Делаем переход
                offset = len(result[0])


                self.pos += offset
                if token_type == token_types["NEXTLINE"]:
                    self.linepos[0] += 1
                    self.linepos[1] = 0
                else:
                    self.linepos[1] += offset

                if token_type == token_types["INLINE-COMMENT"]:
                    self.comments.append(Comment(result[0][2:], lineno=self.linepos[0], linepos=self.linepos[1] - len(result[0]) + 1))
                    self.linepos[0] += 1
                    self.linepos[1] = 0
                    return True

                self.tokens.append(token)
                return True

        raise Exception(f'На позиции ({self.linepos[0]}, {self.linepos[1]}) обнаружена ошибка')
