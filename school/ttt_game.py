from bots import *
from tkinter import Tk, Canvas


class TicTacToe:
    def __init__(self, size):
        self.turn = True
        self.the_grid = [[-1] * size for _ in range(size)]
        self.chosen = [[False] * size for _ in range(size)]
        self.size = size
        self.length = size

        self.bot = Bot1()
        self.moves = []

        self.scale = 150
        self.dim = size * self.scale
        self.root = Tk()
        self.root.geometry(f'{self.dim}x{self.dim}')

        self.canvas = Canvas(self.root, width=self.dim, height=self.dim)
        self.canvas.pack()

        self.create_lines()
        self.binds()
        
        self.root.mainloop()

    def move(self, row, col, bot=False):
        if self.chosen[row][col]:
            print('cant place there')
            return

        self.the_grid[row][col] = int(self.turn)
        self.moves.append((row, col))
        self.chosen[row][col] = True
    
        x, y = (col + .5) * self.scale, (row + .5) * self.scale
        self.canvas.create_text(x, y, text='x' if self.turn else 'o',
                                font=('Helvetica', self.scale), fill='black', tags=('pieces',))

        print(check_win(tuple(self.moves), self.length, self.size))
        self.turn = not self.turn

        if not bot:
            return self.move(*self.bot.move(self), bot=True)

    def reset(self):
        self.root.destroy()
        TicTacToe.__init__(self, self.size)

    def create_lines(self):
        for i in range(1, self.size + 1):
            a, b = i * self.scale, i * self.scale
            self.canvas.create_line(a, 0, a, self.dim, fill='black', tags=('lines',))
            self.canvas.create_line(0, b, self.dim, b, fill='black', tags=('lines',))

    def binds(self):
        b = [(self.root, 'Return', lambda e: self.reset()),
             (self.canvas, 'Button-1', lambda e: self.move(e.y // self.scale, e.y // self.scale))]

        for item, seq, func in b:
            item.bind(f'<{seq}>', func)


if __name__ == '__main__':
    TicTacToe(3)
