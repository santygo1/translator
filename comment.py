class Comment:
    '''
    Комментарий содержит контент и позицию где встретился в исходном файле
    Можно достать из лексера
    Не является так таковым токеном: в результате работы лексера его нельзя увидеть в tokens а можно достать из comments
    '''

    def __init__(self, content:str, lineno, linepos):
        self.content = content.strip()
        self.lineno = lineno
        self.linepos = linepos

    def __repr__(self):
        return f'<Comment: content={self.content}, pos=({self.lineno}, {self.linepos})>'
