from pieces import Pawn, Rook, Knight, Bishop, Queen, King
from tkinter import Tk, Canvas


class Board:
    order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]

    def __init__(self, root, canvas, dim):
        self.sx = self.sy = dim // 8
        self.root, self.canvas = root, canvas

        self.DISPLAY = True
        self.LIGHT, self.DARK, self.MOVE = '#E8D3BB', '#9A715E', '#FF0000'

        self.array = [
            [piece(self, 'b', (0, i)) for i, piece in enumerate(self.order)],
            [Pawn(self, 'b', (1, i)) for i in range(8)],
            *[[None] * 8 for _ in range(4)],
            [Pawn(self, 'w', (6, i)) for i in range(8)],
            [piece(self, 'w', (7, i)) for i, piece in enumerate(self.order)]
        ]
        self.turn = True
        self.piece, self.piece_moves = None, []
        self.check = False

        self.display()

    def display(self):
        for r, row in enumerate(self.array):
            y = r * self.sy
            y1 = y + self.sy
            for c, sq in enumerate(row):
                x = c * self.sx
                self.canvas.create_rectangle(x, y, x + self.sx, y1, fill=self.DARK if (r + c) % 2 else self.LIGHT,
                                             tags=('squares',))
                # images are drawn in the constructor for each piece
        self.canvas.tag_lower('squares')

    def display_moves(self):
        for r, c in self.piece_moves:
            self.canvas.create_oval(*self.circle_location(*self.canvas_location_center(r, c)),
                                    fill=self.MOVE, tags=('moves',))
        self.canvas.tag_raise(self.piece.drawing)

    def circle_location(self, x, y):
        mx, my = self.sx / 4, self.sy / 4
        return x - mx, y - my, x + mx, y + my

    def canvas_location_center(self, r, c): return (c + .5) * self.sx, (r + .5) * self.sy

    def canvas_location(self, r, c): return c * self.sx, r * self.sy

    def grid_location(self, x, y): return y // self.sy, x // self.sx

    def select(self, event):
        r, c = self.grid_location(event.y, event.y)
        piece = self.array[r][c]
        if piece is None:
            return

        if (piece.color == 'b') is self.turn:
            return

        self.piece, self.piece_moves = piece, piece.get_moves()
        self.display_moves()

    def select_check(self, event):
        pass

    def drag(self, event):
        if self.piece is not None:
            self.canvas.moveto(self.piece.drawing,
                               event.y - self.piece.width / 2, event.y - self.piece.height / 2)

    def deselect(self, event):
        if self.piece is None:
            return

        r, c = self.grid_location(event.y, event.y)
        self.canvas.delete('moves')
        if (r, c) not in self.piece_moves or (r, c) == self.piece.coords:
            self.canvas.moveto(self.piece.drawing, *self.canvas_location(*self.piece.coords))
            self.piece, self.piece_moves = None, []
            return

        self.piece.move(r, c)
        self.turn = not self.turn

        self.piece, self.piece_moves = None, []

    def deselect_check(self, event):
        pass

    def start(self):
        self.canvas.bind('<ButtonPress>', lambda e: self.select_check(e) if self.check else self.select(e))
        self.canvas.bind('<ButtonRelease>', lambda e: self.deselect_check(e) if self.check else self.deselect(e))
        self.canvas.bind('<Motion>', self.drag)
        self.root.mainloop()


if __name__ == '__main__':
    d = 800
    rt = Tk()
    rt.geometry(f'{d}x{d}')

    canv = Canvas(rt, height=d, width=d)
    canv.pack()

    Board(rt, canv, d).start()
