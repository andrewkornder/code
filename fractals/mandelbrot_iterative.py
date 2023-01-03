from tkinter import Tk, Canvas, PhotoImage
from os import listdir
import cv2


d = 2


def mandelbrot(z, c):
    return z ** d + c


class Window:
    def __init__(self, width, height, x0, x1, y0, y1, threshold, save=True):
        self.auto = 0
        self.i = 0
        self.save = save

        self.root = Tk()
        self.root.geometry(f'{width}x{height}')

        self.canvas = Canvas(self.root, width=width, height=height, bg='black')
        self.canvas.pack()

        self.image = PhotoImage(width=width, height=height)
        self.canvas.create_image(0, 0, image=self.image, state="normal", anchor='nw')

        self.width, self.height = width, height

        self.xs, self.ys = (x1 - x0) / width, (y1 - y0) / height
        self.cs = 255 / (threshold * threshold)

        self.x0, self.x1, self.y0, self.y1 = x0, x1, y0, y1
        self.threshold = threshold

        self.data = [[complex(0, 0)] * self.width for _ in range(self.height)]

        self.root.bind('<Return>', lambda *_: self.iterate())
        self.root.bind('<space>', lambda *_: self.toggle())

        self.iterate()
        self.root.mainloop()

    def color(self, z):
        return f'#0000{int(self.cs * max(0, self.threshold * self.threshold - (z * z.conjugate()).real)):02x}'

    def iterate(self):
        print(f'\rstarting {self.auto:<4}', end='')

        for y in range(self.height):
            y_i = self.y0 + y * self.ys
            for x in range(self.width):
                x_i = self.x0 + x * self.xs
                value = mandelbrot(self.data[y][x], complex(x_i, y_i))
                self.data[y][x] = value
        self.i += 1

        self.image.put(' '.join('{' + ' '.join(map(self.color, row)) + '}' for row in self.data))
        if self.save:
            self.image.write(f'images/mandelbrot_{self.i:>04}.png', format='png')

        if self.auto:
            self.auto -= 1
            self.iterate()

    def toggle(self):
        self.auto += 10


def convert_frames_to_video(folder, output, fps):
    files = list(map(lambda file: f'{folder}/{file}', sorted(listdir(folder))))
    frames = map(cv2.imread, files)

    video = cv2.VideoWriter(output, cv2.VideoWriter_fourcc(*'DIVX'), fps, cv2.imread(files[0]).shape[1::-1])
    [video.write(frame) for frame in frames]
    video.release()


if __name__ == '__main__':
    convert_frames_to_video('./images', 'mandelbrot_video.mp4', 5)
    input(1)

    xa, xb = -2, 1
    ya, yb = 1.3, -1.3
    Window(1920 - 100, 1080 - 100, xa, xb, ya, yb, 2)
