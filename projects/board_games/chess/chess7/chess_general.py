import tkinter

# TODO:
"""
flesh out visuals
create actual pieces
write check and turn-based moves
en passant + other weird rules
50 move rule
castling
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


class Piece:
    @staticmethod
    def check_bounds(r, c):
        return 0 <= r < 8 and 0 <= c < 8

    @staticmethod
    def get_path(name, c):
        return f'../{"white" if c == 1 else "black"}{name}.png'

    def __init__(self, board, r, c, color, name, text=None):
        self.board, self.window = board, board.window
        self.r, self.c = r, c
        self.color = color

        self.image = tkinter.PhotoImage(file=self.get_path(name, color))
        self.drawing = self.window.draw_image(r, c, self.image)
        self.text = text if text else name[0]
        if color:
            self.text = self.text.upper()

    def open_square(self, r, c):
        p = self.board.arr[r][c]
        return p is None or p.color != self.color

    def move(self, r1, c1):
        self.board.arr[r1][c1] = self
        self.board.arr[self.r][self.c] = None
        self.r, self.c = r1, c1

        x, y = self.window.get_window_loc(r1, c1)
        self.window.canvas.moveto(self.drawing, x, y)

    def __str__(self):
        return self.text

    @property
    def coords(self):
        return self.r, self.c


class Board:
    def __init__(self, layout: list[list]):
        colors = [(240, 217, 181), (181, 136, 99)]
        self.window = Window(800, 800, 8, 8, colors)

        binds = [
            ('root', 'q', self.destroy),
            ('canvas', 'ButtonPress-1', lambda e: self.press(e.x, e.y)),
            ('canvas', 'ButtonRelease-1', lambda e: self.release(e.x, e.y)),
            ('canvas', 'Motion', lambda e: self.drag(e.x, e.y))
        ]

        self.window.bind_all(binds)

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

        self.window.run()

    @staticmethod
    def get_notation(r, c): return f'{"abcdefgh"[c]}{r + 1}'

    def print_board(self):
        for row in self.arr:
            print(' '.join(str(p) if p else '_' for p in row))

    def draw_possible_moves(self):
        for r, c in self.selection.get_moves():
            self.window.draw_square(*self.window.get_window_loc(r, c), tags=('moves',))
        self.window.canvas.tag_raise('images')

    def press(self, x, y):
        r, c = self.window.get_board_loc(x, y)
        self.selection = self.arr[r][c]
        if self.selection is None:
            print(f'empty square at {self.get_notation(r, c)}')
            return

        self.draw_possible_moves()

    def drag(self, x, y):
        if self.selection is None:
            return

        self.window.canvas.moveto(self.selection.drawing, x - self.window.sx / 2, y - self.window.sy / 2)

    def release(self, x, y):
        r, c = self.window.get_board_loc(x, y)

        self.window.delete('moves')
        if self.selection is None or (r, c) == self.selection.coords:
            return

        self.selection.move(r, c)
        self.selection = None

    def destroy(self, *_):
        self.window.root.destroy()
