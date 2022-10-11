import numpy as np
import pandas as pd
import random_board as rb
from stockfish import Stockfish

engine = Stockfish(path='stockfish_15/stockfish.exe')
engine.set_depth(15)
data = pd.DataFrame(data=['rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'],
                    columns=['board'], index=[0])
y = pd.Series([0.2])
y1 = pd.Series(['d2d4'])


def create_data():
    for i in range(10):
        board = rb.generate()
        data.loc[-1] = board
        engine.set_fen_position(board)
        ev = engine.get_evaluation()
        if ev['type'] == 'mate':
            ev['value'] = 10000
        y.loc[-1] = ev['value']
        y1.loc[-1] = engine.get_best_move(1000)
        print(i)


create_data()
print(data + y + y1)
