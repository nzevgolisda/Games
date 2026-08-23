
class Square:
    def __init__(self, sq):
        self.sq = sq
        self.pieces = []
    def __str__(self):
        if self.pieces == []:
            return self.sq
            #return '_ '
        else:
            return self.pieces[0].name
            #return self.pieces[0].value
class Piece:
    def __init__(self, name, sq):
        self.name = name
        self.sq = sq
        self.value = 'No'
        self.tookPiece = False
        self.take_value()
    def take_value(self):
        self.names = [' R', ' K', ' B', ' Q', 'Kg', ' B', ' K', ' R', ' p']
        self.values = ['5 ', '3 ', '4 ', '9 ', '40', '4 ', '3 ', '5 ', '1 ']
        
        for i in range(len(self.names)):
            if self.name == self.names[i]:
                self.value = self.values[i]
    def __str__(self):
        return str(self.name)+str(self.sq)
class Board:
    def __init__(self):
        self.initPaper()
        self.initSquares()
        self.initPieces()
        self.insertPieces()
        print(self)
    def initPaper(self):
        self.moves = 0
        self.match_paper = []
        for j in range(10):
            self.match_paper.append(['', ''])
    def initSquares(self):
        self.letters = 'abcdefgh'+'ABCDEFGH'
        self.size = [6, 7] #row x col
        self.board = []
        for i in range(self.size[0]-1, -1, -1): #row
            row = []
            for j in range(self.size[1]): #col
                sq = self.letters[j] + str(i+1)
                square = Square(sq)
                row.append(square)
            self.board.append(row) 
    def initPieces(self):
        self.white = []
        self.black = []
        self.names = [' R', ' N', ' B', ' Q', ' K', ' B', ' N', ' R',]
        
        # Pawns
        for i in range(self.size[1]):
            #white
            row = 2
            square = self.letters[i] + str(row)
            p = Piece(' p', square)
            p.player = 'White'
            self.white.append(p)
            # black
            row = self.size[0]-1
            square = self.letters[i] + str(row)
            p = Piece(' p', square)
            p.player = 'Black'
            self.black.append(p)
        # Pieces
        for i in range(self.size[1]):
            # white
            row = 1
            name = self.names[i]
            square = self.letters[i] + str(row)
            p = Piece(name, square)
            p.player = 'White'
            self.white.append(p)
            # black
            row = self.size[0]
            name = self.names[i]
            square = self.letters[i] + str(row)
            p = Piece(name, square)
            p.player = 'Black'
            self.black.append(p)
    def findSquare(self, s):
        i = int(self.letters.index(s[0]))
        j = self.size[0]-int(s[1])
        return i, j
    def insertPieces(self):
        #White
        for n in range(len(self.white)):
            p = self.white.pop()
            s = p.sq
            i, j = self.findSquare(s)
            self.board[j][i].pieces.append(p)
        #Black
        for m in range(len(self.black)):
            p = self.black.pop()
            s = p.sq
            i, j = self.findSquare(s)
            self.board[j][i].pieces.append(p)
    
    def startSquare(self, player):
        a = str(input('Give starting square for '+str(player)+': '))
        i, j = self.findSquare(a)
        square = self.board[j][i]
        return square
    def endSquare(self, player):
        a = str(input('Give ending square for '+str(player)+': '))
        i, j = self.findSquare(a)
        square = self.board[j][i]
        return square
    def get_piece(self, player):
        square = self.startSquare(player)
        pieces = square.pieces
        while pieces == [] or pieces[0].player != player:
            print('Empty square or invalid player.')
            square = self.startSquare(player)
            pieces = square.pieces
        return square
    def get_square(self, player):
        square = self.endSquare(player)
        pieces = square.pieces
        while len(pieces)>0 and pieces[0].player == player:
            print('Invalid player.')
            square = self.endSquare(player)
            pieces = square.pieces
        return square
    
    def trackMove(self, sq1, sq2, player):
        move = self.match_paper[self.moves]
        p1 = sq1.pieces[0]
        a, b = sq1.sq, sq2.sq

        i = ['White', 'Black'].index(player)
        if len(sq2.pieces) > 0:
            p1.tookPiece = True
            s = a+'x'+b
        else:
            s = a+'-'+b
        if p1.name != ' p':
            move[i] = p1.name+s
        else:
            move[i] = s
        if p1.player == 'Black':
            self.moves+=1
    def exchange(self, sq1, sq2, player):
        p1 = sq1.pieces.pop()
        if p1.tookPiece == True:
            p2 = sq2.pieces.pop()
            if player == 'White':
                self.black.append(p2)
            elif player == 'Black':
                self.white.append(p2)
        p1.sq = sq2.sq
        sq2.pieces.append(p1)
    def move(self, player):
        sq1 = self.get_piece(player)
        sq2 = self.get_square(player)
        
        self.trackMove(sq1, sq2, player) # match paper completion
        self.exchange(sq1, sq2, player) # Make the move of p1 to the sq2
        print(self)
        self.show_deceased()
    
    def show_deceased(self):
        w = []
        for p in self.white:
            w.append(str(p))
        b = []
        for p in self.black:
            b.append(str(p))
        print(str(w)+': White')
        print(str(b)+': Black')
    def __str__(self):
        w = []
        paper = self.match_paper
        row = 'Game'+' '*(3*(self.size[1]+3)-4)
        w.append(row+str(paper[0]))
        for i in range(self.size[0]):
            row = ''
            row_list = self.board[i]
            for j in range(self.size[1]):
                square = row_list[j]
                row += str(square) + ' '
            row += ' | '+str(self.size[0]-i) +' |   '
            w.append(row+str(paper[i+1]))

        k =self.size[0]
        row = '-- '*self.size[1]+' '*9+str(paper[k])
        w.append(row)
        row = ''
        for i in range(self.size[1]):
            row += ' ' +str(self.letters[i].upper()) + ' '
        w.append(row+' '*9 +str(paper[k+1]))
        
        for j in range(k+2, len(paper)):
            row = ' '*30 + str(paper[j])
            w.append(row)
        w1 = ''
        n = len(w)
        for i in range(n):
            w1 += w[i]+'\n'
        return w1

b = Board()
while True:
    b.move('White')
    b.move('Black')
