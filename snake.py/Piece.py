class Piece:
    def __init__(self, value, square):
        self.value = value
        self.square = square
    def __str__(self):
        if self.value == 0:
            return str(self.square)+str('|')
        elif self.value == 1:
                return '*|'
        elif self.value == 2:
            return 's |'
             
    ##def __str__(self):
    ##    if self.value == 0:
    ##        return ' '+str(self.square)+' | '
    ##    else:
    ##        return '  '+str(self.value)+' | '