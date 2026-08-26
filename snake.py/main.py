from Piece import Piece
from Board import Board
import keyboard

board = Board()
print(board)
board.addHeadPiece()

while True:
    board.move()
