from pieces import *
from chess_general import Board

if __name__ == '__main__':
    layout = [
        [Pawn] * 8,
        [Pawn] * 8,
        ]
    Board(layout)