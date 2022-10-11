import tkinter
from pprint import pprint


class Board:
    def __init__(self):
        self.w, self.h = 8, 8
        self.red, self.black = '#dd2222', '#000000'
        self.null = ''

        self.arr = []
        self.moves = [7, 9, -7, -9]
        self.captures = [2 * a for a in self.moves]

        self.turn = True

        self.create_arr()
        pprint(self.arr)
        self.display()

    def create_arr(self):
        for i in range(self.w * self.h):
            r = int(i / self.w)
            value = self.black if r < 3 else (self.red if r > 4 else self.null)
            self.arr.append(value if (r + i % self.w) % 2 else self.null)

    def display(self):
        for i in range(self.h):
            y = i * s
            y1 = y + s
            for j in range(self.w):
                value = self.arr[i * 8 + j]
                x = j * s
                x1 = x + s
                switch = (i + j) % 2

                canvas.create_rectangle(x, y, x1, y1,
                                        fill=['#ff1111', '#111111'][
                                            switch], activefill='#FFEB3B')

                if value != '':
                    canvas.create_oval(x + 10, y + 10, x1 - 10, y1 - 10,
                                       fill=value, activefill='#ddc919')


def on_press(event):
    row, col = int(event.y / s), int(event.y / s)
    idx = row * 8 + col

    holding = game.arr[idx], idx



if __name__ == '__main__':
    s = 100
    root = tkinter.Tk()
    root.geometry('800x800')
    canvas = tkinter.Canvas(root, width=800, height=800)
    canvas.pack()

    game = Board()
    holding = None

    canvas.bind('<Button-1>', on_press)
    canvas.bind('<Motion>', move_holding)

    root.mainloop()
