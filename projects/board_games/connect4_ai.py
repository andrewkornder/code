import random
import tkinter
from pprint import pprint

colors = ['#111122', '#ee2244']
background = '#2211ee'


def printarr(arr):
    for a in arr:
        print(' '.join(map(str, a)).replace(board.red, 'r').replace(
            board.black, 'b').replace(background, '_'))
    print('\n\n')


class Bot:
    def simulate(self, args, it):
        if it == 3:
            return 0

        ot, arr, m, t, place = args

        if board.check_win(arr, t):
            if t == ot:
                return 1
            else:
                return -1

        legal = [a for a in range(board.width) if place[a] >= 0]
        arr[m][place[m]] = t
        place[m] -= 1
        nt = board.red if t == board.black else board.black
        s = []

        for move in legal:
            result = self.simulate([ot, arr, move, nt, place], it + 1)
            s.append(result)

        return not (-1 in s)

    def get_move(self, turn, orig):
        p = []
        for move in [a for a in range(board.width) if board.place[a] != -1]:
            args = [turn, [a[:] for a in orig], move, turn, board.place[:]]
            result = self.simulate(args, 1)
            p.append((move, result))

        p.sort(key=lambda y: y[1])
        pprint(p)
        chosen = p[-1]
        return chosen[0]

    @staticmethod
    def avoid_losing(turn, orig):
        legalA = [a for a in range(board.width) if board.place[a] > -1]
        for m in legalA[:]:
            arr = [a[:] for a in orig]
            place = board.place[:]
            arr[m][place[m]] = turn
            place[m] -= 1
            nt = board.red if turn == board.black else board.black
            if board.check_win(arr, turn):
                print(f'{m} is a win for {turn}')
                return m
            for m2 in [a for a in range(board.width) if place[a] > -1]:
                arr2 = [a[:] for a in arr]
                arr2[m2][place[m2]] = nt

                if board.check_win(arr2, nt):
                    printarr(arr2)

                    legalA.remove(m)
                    break

        print(legalA)
        if not len(legalA):
            return random.choice(legalA)
        return random.choice(legalA)

    def turn(self, turn):
        m = self.avoid_losing(turn, board.arr)
        board.arr[m][board.place[m]] = turn
        board.place[m] -= 1
        if board.check_win(board.arr, turn):
            end_game(['red', 'black'][board.turn == '#111122'])
            return
        board.turn = board.red if board.turn == board.black else board.black
        board.display()


class Board:
    def __init__(self, width=7, height=6, hex_values=None):
        if hex_values is None:
            hex_values = colors
        canvas.create_rectangle(335, 100, 1050, 700, fill='#777777')

        self.black = hex_values[0]
        self.red = hex_values[1]

        self.width = width
        self.height = height

        self.turn = self.black
        self.arr = [[background for _ in range(height)] for _ in range(width)]
        self.circles = []
        self.diag_coords = get_diagonals(width, height)
        self.place = [height - 1] * width

    def press(self, event):
        if not (350 <= event.y <= 1050):
            if event.y > 1050:
                print(self.check_win())
                nt = self.red if self.turn == self.black else self.black
                print(self.check_win(t=nt))
            return

        x = event.y - 350
        col = int(x / size)
        row = self.place[col]
        if row == -1:
            return

        self.place[col] -= 1

        self.arr[col][row] = self.turn
        if self.check_win():
            end_game(['red', 'black'][self.turn == '#111122'])
            return
        self.turn = self.red if self.turn == self.black else self.black

        self.display()

        bot.turn(self.turn)

    def display(self):
        for c in self.circles:
            canvas.delete(c)
        self.circles = []

        for i, column in enumerate(self.arr):
            x = i * size + 350
            x1 = x + csize
            for j, square in enumerate(column):
                y = j * size + 107
                y1 = y + csize
                self.circles.append(
                    canvas.create_oval(x, y, x1, y1, fill=square))

    def check_win(self, arr=None, t=None):
        if arr is None:
            arr = self.arr
        if t is None:
            t = self.turn
        diagonals = [[arr[x][y] for x, y in diag] for diag in self.diag_coords]
        for xy in diagonals:
            if sublist_exists(xy, [t] * 4):
                return True

        for A in [arr, self.rotate()]:
            for sublist in A:
                if sublist_exists(sublist, [t] * 4):
                    return True
        return False

    def rotate(self):
        return [[self.arr[j][i] for j in range(self.width)] for i in
                range(self.height)]


def get_diagonals(w, h):
    d = [[(j + i, j) for j in range(w - i)] for i in range(w)][1:]
    d += [[(j, j + i) for j in range(h - i)] for i in range(h)]
    d += [[(w - a - 1, b) for a, b in d2] for d2 in d]

    return d


def sublist_exists(l, sublist):
    if len(sublist) > len(l):
        return False
    for i in range(board.height - 3):
        if sublist == l[i:i + 4]:
            return True
    return False


def end_game(won):
    print(f'{won} won the game')
    board.display()
    # canvas.unbind('<Button-1>')


if __name__ == '__main__':
    dimX = 1400
    dimY = 800
    size = 100
    csize = 85

    root = tkinter.Tk()
    root.title('connect 4')
    root.geometry(f'{dimX}x{dimY}')

    canvas = tkinter.Canvas(root, width=dimX, height=dimY, bg=background)
    canvas.pack()

    board = Board()
    board.display()
    bot = Bot()

    canvas.bind('<Button-1>', board.press)

    root.mainloop()
