from tkinter import Tk, Canvas, Button, Label


class App:
    def __init__(self):
        self.running = False
        self.frame_rate = 10

        self.root = Tk()
        self.root.geometry('{}x{}'.format(1400, 1100))

        self.start_stop = Button(self.root, text='start/stop', command=self.pause)
        self.start_stop.grid(row=0, column=0)

        self.canvas = Canvas(self.root, width=1000, height=1000, bg='white')
        self.canvas.grid(row=1, column=0, rowspan=3)

        self.text_display = Label(self.root, text='', height=17)
        self.text_display.grid(row=1, column=1)

    def pause(self):
        self.running = not self.running

    def run(self):
        self.root.mainloop()