import tkinter


class Switch:
    def __init__(self, root, state=0, height=300, width=600, offset=10, colors=['blue', 'red']):
        self.__dict__.update({k: v for k, v in locals().items() if k != 'self'})

        self.colors = colors
        self.widget = tkinter.Canvas(root, bg=colors[1], height=height, width=width)
        self.coords = [(self.offset, self.offset, height - self.offset, 0.5 * width - self.offset),
                       (0.5 * self.width - self.offset, self.offset, self.width - self.offset, height - self.offset)]

        self.circle = self.widget.create_oval(*self.coords[state], outline='', fill='white')
        self.widget.bind('<Button-1>', lambda x: self.change_state())

    def change_state(self):
        self.widget['bg'] = self.colors[self.state]
        self.state = not self.state
        self.widget.delete(self.circle)
        self.circle = self.widget.create_oval(*self.coords[self.state], outline='', fill='white')

    def get(self): return self.state


root = tkinter.Tk()
root.geometry('600x300')

Switch(root).widget.pack()
root.mainloop()
