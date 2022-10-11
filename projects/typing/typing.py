from timeit import default_timer as timer
import tkinter
from PIL import Image
import random
import string


def rgb_to_hex(rgb):
    return '#' + ''.join(f'{a:x}' for a in rgb)


class Keyboard:
    def __init__(self, canvas, x, y):
        self.image = tkinter.PhotoImage(file='keyboard.png')
        self.size = (768, 250)
        self.x, self.y = x, y

        self.canvas = canvas
        self.canvas.create_image(x, y, image=self.image, anchor=tkinter.CENTER)


class TypingWindow:
    def __init__(self, window, w, h, words):
        self.window = window
        self.canvas = tkinter.Canvas(window, width=w, height=h, bg='grey')
        self.canvas.pack()

        # assuming minimum height of 1000 with 250 for the keyboard at the bottom, using 50 for padding
        self.keyboard = Keyboard(self.canvas, w / 2, h - 300)

        self.words = words
        self.text = []  # list of tkinter canvas objects so i can delete them on start of new attempt

        self.window.bind('<Key>', self.type)
        self.window.bind('<Return>', self.start)

        self.font = ('Niagara Bold', 15)
        self.text_x, self.text_y = 500, 300  # ?!!?!
        self.timer = None
        self.current_text = self.get_words()
        self.cursor = 0  # index of self.current_text that the user is current typing
        self.start()

    def get_words(self, length=10):
        return " ".join(random.sample(self.words, length))

    def type(self, event):
        key = event.keysym
        if key not in 'abcdefghijklmnopqrstuvwxyz,./;1234567890' or key == 'Return':
            print(key)
            return

        if self.timer is None:
            self.timer = timer()

        if self.current_text[self.cursor] == key:
            self.draw_letter(self.cursor)

            self.cursor += 1
            if self.cursor == len(self.current_text):
                self.timer = timer() - self.timer()
                print(self.timer)  # display the time
                self.start()

    def start(self, *a):
        self.canvas.delete(*self.text)
        self.text = []

        self.current_text = self.get_words()
        self.cursor = 0
        self.timer = None

        self.draw_text(self.current_text)

    def draw_text(self, text):  # only really for the start of the game
        self.text.append(
            self.canvas.create_text(self.text_x, self.text_y, text=text, font=self.font, fill='light grey'))

    def draw_letter(self, index):
        text = self.current_text[:index + 1] + ' ' * (len(self.current_text) - self.cursor)
        self.text.append(self.canvas.create_text(self.text_x, self.text_y, text=text, font=self.font, fill='white'))


class App:
    def __init__(self, w, h):
        self.r = tkinter.Tk()
        self.r.geometry(f'{w}x{h}+0+0')
        self.r.configure(background='grey')

        self.window = TypingWindow(self.r, w, h, self.get_words())
        self.r.mainloop()

    @staticmethod
    def get_words(file=r'E:\all\code\projects\wordle2 - finished\answers.txt'):
        return open(file).read().replace('"', '').split(',')


if __name__ == '__main__':
    app = App(1000, 1000)
