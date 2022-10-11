import tkinter
from PIL import Image, ImageTk

pieces = list('rnbqkbnr')
piecesFromIndex = dict(zip(range(8), pieces))


def ms():
    rm = [-8, -1], True
    bm = [-7, -9], True
    qm = [-7, -8, -9, -1], True
    km = [-7, -8, -9, -1, 1, 7, 8, 9], False
    piecenames_trunc = 'rbqkbr'
    return dict(zip(piecenames_trunc, [rm, bm, qm, km, bm, rm]))


class Board:
    def __init__(self, size=8, colors=((232, 211, 187), (154, 113, 94))):
        self.size = size
        self.arr = []
        self.king_pos = {'w': 60, 'b': 4}
        self.in_check = {'w': False, 'b': False}
        self.can_castle = {'w': [True, True], 'b': [True, True]}
        images = []
        for l in list('prnbkq'):
            images.append('white' + l)
            images.append('black' + l)
        self.imgs = {}

        for i, image in enumerate(images):
            curr = Image.open(image + '.png')
            curr = curr.convert("RGBA")

            self.imgs[image[0] + image[-1]] = ImageTk.PhotoImage(
                curr.resize((block, block)))

        self.colors = ["#%02x%02x%02x" % i for i in colors]
        self.red = []
        self.items = [None for _ in range(64)]
        self.double_moves = []
        self.moveset = ms()
        for a in range(size):
            for b in range(size):
                v = ' ' if a not in (0, 7) else piecesFromIndex[b]
                v = v if a not in (1, 6) else 'p'
                if v == 'p':
                    self.double_moves.append(a * s + b)
                if a in (0, 1):
                    c = 'b'
                elif a in (6, 7):
                    c = 'w'
                else:
                    c = ' '
                self.arr.append(c + v)
        self.draw()

    def check(self, pN):
        print('in check()')
        threats_list = list('rbn')
        c, p = list(pN)
        kp = self.king_pos[turn]
        threats = []
        m2 = []
        for a in [self.generateM(c + a, kp) for a in threats_list]:
            for move in a:
                curr = self.arr[move]
                cc, cp = list(curr)
                if cc not in [' ', c]:
                    threats.append((curr, move))
        selfpieces = [i for i in range(64) if self.arr[i][0] == turn]
        for piece in selfpieces:
            curr = self.arr[piece]
            c_board = self.arr[:]
            moves = self.generateM(curr, piece)
            for m in moves:
                self.arr[m] = self.arr[piece]
                self.arr[piece] = '  '
                temp_bool = True
                for threat in threats:
                    for pos in self.generateM(threat[0], threat[1]):
                        if self.arr[pos] == turn + 'k':
                            temp_bool = False
                if temp_bool:
                    m2.append((piece, m))
                self.arr = c_board[:]

        for a in m2:
            self.red.append(a[0])
            self.red.append(a[1])

        if not len(m2):
            # canvas.create_text(400, 400, font=('Consolas', 100), text='CHECKMATE')
            print('checkmate liberal')
            exit()

        return m2

    def text(self, x, y, t):
        canvas.create_text(x, y, text=t, font=("Consolas", 20))

    def display(self):
        for row, v in enumerate(self.arr):
            for p in v:
                print(p, end='  ')
            print('  ', s - row)

    def get_xy(self, row, col):
        x, y = col * block, row * block
        x1, y1 = x + block, y + block
        return x, y, x1, y1

    def rc(self, i):
        row = int(i / self.size)
        col = i % self.size
        return row, col

    def draw(self, pass_bool=False):
        canvas.delete('all')
        for i in range(64):
            a = self.arr[i]
            row, col = self.rc(i)
            x, y, x1, y1 = self.get_xy(row, col)

            canvas.create_rectangle(x, y, x1, y1,
                                    fill=self.colors[(row + col) % 2])

            x2, y2 = self.textxy((x, y, x1, y1))
            if a != '  ':
                self.items[i] = canvas.create_image(x2, y2, image=self.imgs[a])
        self.red = []

    def textxy(self, xy):
        x, y, x1, y1 = xy
        x2 = (x + x1) / 2
        y2 = (y + y1) / 2
        return x2, y2

    def knightMoves(self, idx, pN):
        r, c = self.rc(idx)
        m = []

        for a in (-2, 2):
            ar, ac = r + a, c + a
            for b in (1, -1):
                bc, br = c + b, r + b
                m.append((ar, bc))
                m.append((br, ac))

        m = [(a, b) for a, b in m if
             a in list(range(s)) and b in list(range(s))]
        m = [a * s + b for a, b in m]
        m2 = []
        for v in m:
            n2 = self.arr[v]
            if n2[0] == pN[0]:
                continue
            m2.append(v)
            self.red.append(v)
        return m2

    def pawnMoves(self, idx, pN):
        r, c = self.rc(idx)
        mult = -1 + 2 * (pN[0] == 'b')
        m = [idx + 8 * mult]

        if idx in self.double_moves:
            m.append(idx + 16 * mult)

        for offset in (1, -1):
            n = m[0] + offset
            if self.arr[n] != '  ':
                m.append(n)
        if self.arr[m[0]] != '  ':
            del m[0]

        m2 = []

        for v in m:
            # v = idx + v1
            if not (-1 < v < 64):
                continue
            nr, nc = self.rc(v)
            if abs(nc - c) > 1:
                continue
            n2 = self.arr[v]
            if n2[0] == pN[0]:
                continue
            m2.append(v)
            self.red.append(v)

        return m2

    def generateM(self, pN, idx):
        if pN == '  ':
            print('empty square')
            return []
        elif pN[1] == 'n':
            m = self.knightMoves(idx, pN)
            return m
        elif pN[1] == 'p':
            m = self.pawnMoves(idx, pN)
            return m

        dirs, cont = self.moveset[pN[1]]

        m = []
        if pN[0] == 'b':
            dirs = [-1 * d for d in dirs]

        if cont:
            m = self.contMoves(idx, pN, dirs)
        else:
            for inc in dirs:
                niP = idx + inc
                niN = idx + -1 * inc
                for ni in (niP, niN):
                    if -1 < ni < 64:
                        n2 = self.arr[ni]
                        if n2[0] == pN[0]:
                            continue
                        m.append(ni)
                        self.red.append(ni)
        return m

    def contMoves(self, idx, name, dirs):
        m = []
        if name[1] == 'q':
            nn = name[0] + 'r'
            a = self.contMoves(idx, nn, self.moveset['r'][0])
            nn = nn[0] + 'b'
            b = self.contMoves(idx, nn, self.moveset['b'][0])
            return a + b
        r, c = self.rc(idx)
        for inc in dirs:
            add = idx + inc
            if -1 < add < 64:
                while self.arr[add] == '  ':
                    m.append(add)
                    add += inc
                    if not (-1 < add < 64):
                        add = None
                        break
                if add is not None and self.arr[add][0] != name[0]:
                    m.append(add)

            sub = idx - inc
            if -1 < sub < 64:
                while self.arr[sub] == '  ':
                    m.append(sub)
                    sub -= inc
                    if not (-1 < sub < 64):
                        sub = None
                        break
                if sub is not None and self.arr[sub][0] != name[0]:
                    m.append(sub)
        m2 = []
        for a in m:
            nr, nc = self.rc(a)
            if name[1] == 'r':
                if not (nr != r and nc != c):
                    m2.append(a)
            if name[1] == 'b':
                if (nr + nc) % 2 == (r + c) % 2:
                    m2.append(a)
        return m2

    def promotion(self):
        global chosen, pN
        pN = turn + chosen
        chosen = None

    def on_click(self, event):
        global moves, cp, pN, turn
        col, row = int(event.y / block), int(event.y / block)
        idx = row * s + col
        pN = self.arr[idx]
        if turns_bool:
            if pN[0] != turn:
                moves = 0, []
                print('wrong turn')
                return None
        else:
            turn = pN[0]

        if not self.in_check[turn]:
            moves = idx, self.generateM(pN, idx)
            self.red += moves[1]
        else:
            moves = idx, self.check(idx, pN)
            if idx not in [a for a, b in moves[1]]:
                print('cannot be moved while in check')
                return None
            for a, b in moves[1]:
                if a == idx:
                    self.red.append(b)
        if pN[1] == 'k' and any(self.can_castle[turn]):
            castleK = abs(64 * (turn == 'w') - 2)
            castleQ = abs(64 * (turn == 'w') - 6)
            kingPos = abs(64 * (turn == 'w') - 4)

            l = [castleK, castleQ]
            for i, pos in enumerate(l):
                if not self.can_castle[turn][i]:
                    continue
                cleared = True
                step = -1 if pos < kingPos else 1
                for x in range(kingPos + step, pos + step, step):
                    if self.arr[x] != '  ':
                        cleared = False
                        break
                if cleared:
                    self.red.append(pos)
                    moves[1].append(pos)

        cp = pN
        for i in self.red:
            r, c = self.rc(i)
            x, y, x1, y1 = self.get_xy(r, c)
            canvas.create_rectangle(x, y, x1, y1, fill='red')
            t = self.arr[i]
            if t != '  ':
                im = self.imgs[t]
                x2, y2 = self.textxy((x, y, x1, y1))
                canvas.create_image(x2, y2, image=im)
        print(moves)

    def on_release(self, event):
        global moves, cp, turn, pN, chosen
        cp = None
        old_idx, move_list = moves
        incheck = self.in_check[turn]
        if incheck:
            movesF = []
            movesT = []
            for a, b in move_list:
                movesF.append(a)
                movesT.append(b)

        col, row = int(event.y / block), int(event.y / block)
        idx = row * s + col
        if incheck:
            legal = idx in movesT
        oR, oC = self.rc(old_idx)

        pN = self.arr[old_idx]
        if move_bool:
            self.arr[idx] = pN
            self.arr[old_idx] = '  '
            turn = 'w' if turn == 'b' else 'b'
            self.draw()
            return None

        if not move_list:
            print('no moves')
            return None

        if idx == old_idx:
            print('did not move')
            self.draw()
            return None

        if pN[1] == 'k' and any(self.can_castle[turn]):
            self.can_castle[turn] = [False, False]
        elif pN[1] == 'r' and any(self.can_castle[turn]):
            self.can_castle[turn][oC < col] = False

        elif pN[1] == 'p' and row in (0, 7):
            promote()
            chosen = None
            self.draw()

        if idx in move_list or (incheck and legal):
            next_moves = self.generateM(pN, idx)
            next_turn = 'w' if turn == 'b' else 'b'
            if self.king_pos[next_turn] in next_moves:
                self.in_check[next_turn] = True

            if pN[1] == 'k' and abs(col - oC) > 1:
                if col - oC < 0:
                    rPos = idx - 2
                    nrPos = idx + 1
                else:
                    rPos = idx + 1
                    nrPos = idx - 1
                self.arr[nrPos] = turn + 'r'
                self.arr[rPos] = '  '
            self.arr[idx] = pN
            self.arr[old_idx] = '  '
            turn = 'w' if turn == 'b' else 'b'
            if old_idx in self.double_moves:
                self.double_moves.remove(old_idx)
        else:
            print('illegal move:', idx, move_list)

        self.draw()

    def print_board(self):
        for a in range(s):
            for b in range(s):
                idx = a * s + b
                v = self.arr[idx]
                v = v[1] if v[0] == 'b' else v[1].upper()

                print(v, end=' ')
            print(' ', a)
        print('\n' + ' '.join(list('01234567')))


def drag(event):
    global cp
    if cp is None:
        return None
    if type(cp) == str:
        col, row = int(event.y / block), int(event.y / block)
        canvas.delete(board.items[row * s + col])
        cp = canvas.create_image(event.y, event.y, image=board.imgs[cp]), board.imgs[cp]
    else:
        canvas.delete(cp[0])
        cp = canvas.create_image(event.y, event.y, image=cp[1]), cp[1]


def promote():
    global top
    top = tkinter.Toplevel(root)
    top.geometry("100x400")
    top.title('choose a piece to promote to')
    selection = tkinter.Canvas(top, height=400, width=100, bg='white')
    selection.pack()
    options = list('qrbn')

    for y0 in range(4):
        x, x1 = 0, 100
        y = y0 * 100
        y1 = y + 100
        x2, y2 = board.textxy((x, y, x1, y1))
        selection.create_rectangle(x, y, x1, y1, fill=board.colors[y0 % 2])
        selection.create_image(x2, y2, image=board.imgs[turn + options[y0]])

    selection.bind('<Button-1>', select_promotion)
    top.grab_set()


def select_promotion(event):
    global chosen
    row = int(event.y / 100)
    chosen = list('qrbn')[row]
    board.promotion()
    top.destroy()


def flip_turns():
    global turns_bool
    turns_bool = not turns_bool


def move_any():
    global move_bool
    move_bool = not move_bool


if __name__ == '__main__':
    turns_bool = True
    move_bool = False
    turn = 'w'
    root = tkinter.Tk()
    chosen = None
    root.configure(bg='white')

    dim = 800
    s = 8
    block = int(dim / s)

    root.geometry(str(dim + 200) + 'x' + str(dim))

    canvas = tkinter.Canvas(root, bg='white', width=dim, height=dim)
    canvas.grid(row=0, column=0, rowspan=s)

    use_turns = tkinter.Button(root, bg='white', text='off/on turns',
                               command=flip_turns)
    use_turns.grid(row=0, column=1)

    move_anywhere = tkinter.Button(root, bg='white', text='move anywhere',
                                   command=move_any)
    move_anywhere.grid(row=1, column=1)

    board = Board(size=s)
    cp = None
    board.draw(True)

    canvas.bind('<ButtonPress>', board.on_click)
    canvas.bind('<Motion>', drag)
    canvas.bind('<ButtonRelease>', board.on_release)

    root.mainloop()
