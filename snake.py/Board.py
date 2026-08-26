
import random
from Piece import Piece
import keyboard

class Board:
    def __init__(self):
        self.r = ['1', '2', '3', '4']
        self.m = int(len(self.r))
        self.c = ['a', 'b', 'c', 'd']
        self.n = int(len(self.c))
        self.board = self.getBoard()
    def getBoard(self):
        self.board = []
        for i in range(self.m):
            row = []
            for j in range(self.n):
                s = str(self.c[j]+self.r[i])
                p = Piece(0, s)
                row.append(p)
            self.board.append(row)
        return self.board
    def countNonZero(self):
        k = 0
        for i in range(self.m):
            for j in range(self.n):
                if self.board[i][j].value != 0:
                    k += 1
        return k
    def addHeadPiece(self):
        if self.countNonZero() == 0:
            j = random.randint(0, self.n-1)
            i = random.randint(0, self.m-1)
            p = self.board[i][j]
            if p.value == 0:
                p.value = 2
                p.square = self.c[j]+self.r[i]
        print(self)
        return self
    def getHead(self):
        for i in range(self.m):
            for j in range(self.n):    
                p = self.board[i][j]
                if p.value == 2:
                    return p
    
    def move(self):
        keyboard.add_hotkey('right', lambda: self.rightMove())
        keyboard.add_hotkey('up', lambda: self.upMove())
        keyboard.add_hotkey('left', lambda: self.leftMove())
        keyboard.add_hotkey('down', lambda: self.downMove())
        
        print('Push the arrows to play')
        keyboard.wait('esc')
        return self
    def Shift(self):
        p = self.getHead()
        i = '1234'.find(p.square[1])
        j = 'abcd'.find(p.square[0])
        if i in range(self.m):
            if j == self.n-1:
                print('lost')
            elif j in range(self.n-1):
                p1 = self.board[i][j+1]    
                if p1.value == 0:
                    p1.value = p.value
                    p.value = 0
        return self
    def rightMove(self):
        self.Shift()
        print(self)
        return self
    def upMove(self):
        self.rotate(-1)
        self.Shift()
        self.rotate(1)
        print(self)
        return self
    def leftMove(self):
        self.rotate(-1)
        self.rotate(-1)
        self.Shift()
        self.rotate(1)
        self.rotate(1)
        print(self)
        return self
    def downMove(self):
        self.rotate(1)
        self.Shift()
        self.rotate(-1)
        print(self)
        return self
    
    def rotate(self, k): ## counter-clockwise rotation (+) of board if k = 1
        L = []
        if k == 1:
            for i in range(self.n):
                row = []
                for j in range(self.m):
                    row.append(self.board[j][self.n-1-i])
                L.append(row)
            self.board = L
        elif k == -1:
            for i in range(self.n):
                row = []
                for j in range(self.m):
                    row.append(self.board[self.m-j-1][i])
                L.append(row)
            self.board = L
        self.initSquareValue()
        return self
    def initSquareValue(self):
        for i in range(self.m):
            for j in range(self.n):
                p = self.board[i][j]
                p.square = self.c[j]+self.r[i]
        return self
    
        
    def __str__(self):
        bord = ''
        for i in range(self.m):
            row = '|'
            for j in range(self.n):
                row += str(self.board[i][j])
            bord += row + '\n'
        bord += '*********'*self.n + '\n'
        return bord
