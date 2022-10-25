import tkinter
from pieces import *

# TODO:
"""
write check and turn-based moves
en passant + other weird rules
50 move rule
draws
promotion
"""


def rgb_to_hex(r, g, b): return f'#{r:02x}{g:02x}{b:02x}'


class Window:
    def __init__(self, w, h, rows, cols, colors):
        self.w, self.h = w, h
        self.sx, self.sy = w // rows, h // cols

        self.root = tkinter.Tk()
        self.root.geometry(f'{w}x{h}')

        self.canvas = tkinter.Canvas(self.root, width=w, height=h)
        self.canvas.pack()

        self.draw_board(rows, cols, [rgb_to_hex(*color) for color in colors])  # will always be alternating colors

    def get_window_loc(self, r, c): return self.sx * c, self.sy * r

    def get_board_loc(self, x, y): return y // self.sy, x // self.sx

    def draw_image(self, r, c, image):
        return self.canvas.create_image(self.get_window_loc(r, c), image=image, anchor=tkinter.NW, tags=('images',))

    def move_drawing(self, r, c, drawing):
        self.canvas.moveto(drawing, *self.get_window_loc(r, c))

    def draw_square(self, x, y, w=None, h=None, c='red', tags=()):
        w, h = w if w else self.sx, h if h else self.sy
        return self.canvas.create_rectangle(x, y, x + w, y + h,
                                            fill=c, tags=tags)

    def draw_board(self, rows, cols, colors):
        y = 0
        for i in range(rows):
            x = 0
            for j in range(cols):
                self.draw_square(x, y, self.sx, self.sx, colors[(i + j) % 2], ('background',))

                x += self.sx
            y += self.sy
        self.canvas.tag_lower('background')

    def delete(self, tag):
        self.canvas.delete(tag)

    def bind_all(self, binds):
        for target, event, func in binds:
            self.__dict__[target].bind(f'<{event}>', func)

    def run(self):
        self.root.mainloop()


class Board:
    def __init__(self, layout: list[list], turns=True):
        colors = [(240, 217, 181), (181, 136, 99)]
        self.window = Window(800, 800, 8, 8, colors)

        binds = [
            ('root', 'q', self.destroy),
            ('canvas', 'ButtonPress-1', lambda e: self.press(e.x, e.y)),
            ('canvas', 'ButtonRelease-1', lambda e: self.release(e.x, e.y)),
            ('canvas', 'Motion', lambda e: self.drag(e.x, e.y)),
            ('root', 'r', self.reset_board)
        ]

        self.window.bind_all(binds)

        self.layout = layout
        self.turn_based = turns

        self.arr = [
            [layout[0][i](self, 0, i, -1) for i in range(8)],
            [layout[1][i](self, 1, i, -1) for i in range(8)],
            [None] * 8,
            [None] * 8,
            [None] * 8,
            [None] * 8,
            [layout[1][i](self, 6, i, 1) for i in range(8)],
            [layout[0][i](self, 7, i, 1) for i in range(8)],
        ]

        self.print_board()

        self.selection = None
        self.moves, self.special_moves = [], []
        self.turn = 1

    @staticmethod
    def get_notation(r, c): return f'{"abcdefgh"[c]}{8 - r}'

    def run(self): self.window.run()

    def reset_board(self, *_):
        self.destroy()
        self.__init__(self.layout, turns=self.turn_based)
        self.run()

    def print_board(self):
        print('\n'.join(' '.join(str(p) if p else '_' for p in row) for row in self.arr))

    def draw_possible_moves(self):
        for r, c in self.moves + self.special_moves:
            self.window.draw_square(*self.window.get_window_loc(r, c), tags=('moves',))

        self.window.canvas.tag_raise('images')

    def press(self, x, y):
        r, c = self.window.get_board_loc(x, y)
        self.selection = self.arr[r][c]
        if self.selection is None:
            print(f'empty square at {self.get_notation(r, c)}')
            return

        if self.turn_based and self.turn != self.selection.color:
            print(f'wrong color: {self.selection.color}')
            self.selection = None
            return

        self.special_moves = self.selection.get_special_moves()
        self.moves = self.selection.get_moves()
        self.draw_possible_moves()

        self.window.canvas.tag_raise(self.selection.drawing)

    def drag(self, x, y):
        if self.selection is None:
            return

        self.window.canvas.moveto(self.selection.drawing, x - self.window.sx / 2, y - self.window.sy / 2)

    def release(self, x, y):
        r, c = self.window.get_board_loc(x, y)

        self.window.delete('moves')
        if self.selection is None:
            return

        if (r, c) == self.selection.coords:
            self.window.move_drawing(r, c, self.selection.drawing)
            self.selection = None
            return

        if (r, c) in self.moves:
            self.selection.move(r, c)
        elif (r, c) in self.special_moves:
            self.selection.special_move(r, c)
        else:
            self.window.move_drawing(*self.selection.coords, self.selection.drawing)

            m = ", ".join(self.get_notation(*m) for m in self.moves + self.special_moves)
            print(f'not in list of available moves: {m}')
            self.selection = None
            return

        self.selection = None
        self.turn = -1 + 2 * (self.turn == -1)

    def destroy(self, *_): self.window.root.destroy()


layout = [
    [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook],
    [Pawn] * 8
]

if __name__ == '__main__':
    Board(layout).run()
