import tkinter


class App:
    def __init__(self, w, h, bg='white', fsize=15, title='editor'):
        self.width, self.height = w, h

        self.root = tkinter.Tk()
        self.root.geometry(f'{w}x{h}')
        self.root.title = title

        self.canvas = tkinter.Canvas(self.root, width=w, height=h, bg=bg)
        self.canvas.pack()

        self.bind()

        self.cursor = 0
        self.string = ['']
        self.fsize = fsize

        self.offset = 0  # when scrolling, window will track which row and how far from the top it is
        self.top_row = 0

        self.indent = 30
        self.root.mainloop()

    def write(self, key):
        if key.keysym == 'Return':
            self.string.append('')
            return
        elif key.keysym == 'BackSpace':
            self.string[-1] = self.string[-1][:-1]
            return
        elif 'Shift' in key.keysym:
            print('shift')
            return

        # print(key.__dict__)
        self.string[-1] += key.char
        print('\n'.join(self.string))

        for row in self.string:
            pass

    def bind(self):
        binds = [
            ('Button-1', lambda e: self.set_cursor(e.x, e.y)),
            ('Key', self.write),
        ]

        for seq, func in binds:
            self.root.bind(f'<{seq}>', func)

    def set_cursor(self, x, y):
        pass


if __name__ == '__main__':
    App(800, 800)