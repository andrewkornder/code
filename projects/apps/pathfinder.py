from typing import Any

import tkinter
from pprint import pprint
from time import sleep


class Maze:
    def __init__(self, arr=[], start=(0, 0), end=0):
        self.size, self.arr, self.end, self.start = dim // size, arr, end, start

    def display(self):
        canvas.delete('all')
        for x in range(0, dim, size):
            canvas.create_line(x, 0, x, dim, fill='black')
            canvas.create_line(0, x, dim, x, fill='black')

        for i, row in enumerate(self.arr):
            for j, obj in enumerate(row):
                x, y = (j + 0.5) * size, (i + 0.5) * size
                canvas.create_text(x, y, text=obj, font=('Niagara Bold', 50))


paths = []
size = 125
dim = 625
game_board = Maze(arr=[[' '] * 5 for _ in range(5)], start=(0, 0), end=(4, 4))
canvas = None


def get_moves(loc):
    a, b = loc
    moves = [(a + i, b + j) for i, j in zip([1, -1, 0, 0], [0, 0, 1, -1])]
    moves = [(x, y) for x, y in moves if 0 <= y < game_board.size and 0 <= x < game_board.size]
    return [(x, y) for x, y in moves if game_board.arr[x][y] != 'x']


def find_paths(maze, start, path=None):
    path = path if path else []
    moves = [a for a in get_moves(start) if a not in path]
    if not moves:
        paths.append(path)
        return

    [find_paths(maze, move, path[:] + [move]) for move in moves]


def shortest(maze):
    find_paths(maze, maze.start, path=[maze.start])
    legal = [a for a in paths if a[-1] == maze.end]
    pprint(legal)
    return min(legal, key=lambda x: len(x))


def create_tile(event):
    row, col = event.y // 125, event.y // 125
    game_board.arr[row][col] = 'x'
    game_board.display()


def make_game():
    def show_move(moves, i, current=None):
        if current:
            canvas.delete(current)
        a, b = moves[i]
        x, y = (b + 0.5) * size, (a + 0.5) * size
        obj = canvas.create_text(x, y, text='o', font=('Niagara Bold', 50), fill='red')
        if i != len(moves) - 1:
            root.after(1000, lambda: show_move(moves, i + 1, obj))

    global paths
    path = shortest(game_board)
    show_move(path, 0)
    paths = []


def create_maze():
    global canvas, root
    root = tkinter.Tk()

    root.geometry('{}x{}'.format(size * 5, size * 5))
    canvas = tkinter.Canvas(root, width=size * 5, height=size * 5, bg='white')
    canvas.pack()
    game_board.display()

    canvas.bind('<Button-1>', create_tile)
    root.bind('<Return>', lambda e: make_game())
    root.mainloop()


if __name__ == '__main__':
    create_maze()
