from pieces import *
from chess_general import Board

if __name__ == '__main__':
    layout = [
        [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook],
        [Pawn] * 8,
        ]
    Board(layout)
