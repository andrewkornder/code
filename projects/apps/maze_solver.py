import tkinter
import random
import pprint


def canv_loc_from_index(index):
    col, row = rc_from_index(index)
    x, y = col * dim, row * dim
    return x, y, x + dim, y + dim


def rc_from_index(index):
    return index % size, int(index / size)


def text_loc_from_index(index):
    col, row = rc_from_index(index)
    return (col + 0.5) * dim, (row + 0.5) * dim


class Maze:
    def __init__(self, dimensions, tkinter_object, obstacles=10):
        self.canv = tkinter_object

        self.total = dimensions ** 2
        self.board = [0 for _ in range(self.total)]

        self.obstacles = []
        for _ in range(obstacles):
            i = random.randint(1, self.total - 1)
            while i in self.obstacles:
                i = random.randint(1, self.total - 1)

            self.obstacles.append(i)
            self.board[i] = 1

    def remove_obstacles(self):
        self.board = [0 for _ in range(self.total)]

    def display(self):
        self.canv.delete('all')
        for x in range(0, wd, dim):
            self.canv.create_line(x, 0, x, wd, fill='black')
            self.canv.create_line(0, x, wd, x, fill='black')

        for i, obj in enumerate(self.board):
            img = 'X' if obj else ' '
            x, y = text_loc_from_index(i)
            self.canv.create_text(x, y, text=img, font=('Niagara Bold', 50))

    def get_directions(self, pos, exclude=[]):
        dl = []
        r, c = rc_from_index(pos)
        for inc in [a for a in [-1, 1, -size, size] if a != exclude]:
            ni = pos + inc
            nr, nc = rc_from_index(ni)
            if (nr == r) ^ (nc == c) and 0 <= ni < self.total:
                if not self.board[ni]:
                    dl.append(inc)

        return dl

    def generate_paths(self, start, last, moves, target):
        if start == target:
            print('target found')
            return moves
        dl = self.get_directions(start, last)
        if dl:
            return [self.generate_paths(start + i, -i, moves + [start + i], target) for i in dl]
        return moves

    def find_paths(self, start, exit):
        l = self.generate_paths(start, None, [], exit)
        for id, i in enumerate(l):
            if type(l) == list and len(i) == 1:
                l[id] = i[0]
        print(l)


def on_click(event):
    col, row = int(event.y / dim), int(event.y / dim)
    idx = row * size + col
    board.display()
    pprint.pprint(board.find_paths(0, 24))


def window():
    global root, canvas, board, size, dim, wd

    size = 5
    dim = 100
    wd = dim * size

    root = tkinter.Tk()
    root.geometry(f'{wd}x{wd}')

    canvas = tkinter.Canvas(root, bg='white', width=wd,
                            height=wd)
    canvas.pack()

    canvas.bind('<Button-1>', on_click)

    board = Maze(size, canvas)
    root.mainloop()


window()
