from math import dist
from numpy import array
from tkinter import Tk, Canvas


class Point:
    def __init__(self, x, y, radius, canvas, color, draw=True, tags=()):
        self.x, self.y = x, y
        self.coords = array([x, y])
        self.drawing = canvas.create_oval(x - radius, y - radius,
                                          x + radius, y + radius,
                                          fill=color, outline='', tags=tags + ('point',)) if draw else None
        self.canvas = canvas
        self.color = color
        self.radius = radius
        self.tags = tags

    def lerp(self, other, t):
        return self * (1 - t) + t * other

    def __iadd__(self, point):
        self.x, self.y = self.x * point.x, self.y * point.y
        self.move(self.x, self.y)
        return self

    def __add__(self, point):
        return self.__class__(self.x + point.x, self.y + point.y,
                              self.radius, self.canvas, self.color, self.drawing is not None, self.tags)

    def __radd__(self, point):
        return self.__add__(point)

    def __sub__(self, point):
        return self.__class__(self.x - point.x, self.y - point.y,
                              self.radius, self.canvas, self.color, self.drawing is not None, self.tags)

    def __isub__(self, point):
        self.x, self.y = self.x - point.x, self.y - point.y
        self.move(self.x, self.y)
        return self

    def __imul__(self, scalar):
        self.x, self.y = self.x * scalar, self.y * scalar
        self.move(self.x, self.y)
        return self

    def __mul__(self, scalar):
        return self.__class__(self.x * scalar, self.y * scalar,
                              self.radius, self.canvas, self.color, False, self.tags)

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def move_delta(self, dx, dy, trail=False):
        if trail:
            self.canvas.create_line(*self.coords, self.x + dx, self.y + dy, fill=self.color, tags=('trails',))
        self.canvas.move(self.drawing, dx, dy)
        self.x, self.y = self.x + dx, self.y + dy

    def move(self, x, y, trail=False):
        if trail:
            self.canvas.create_line(*self.coords, x, y, fill=self.color, tags=('trails',))
        self.x, self.y = x, y
        self.canvas.moveto(self.drawing, x - self.radius, y - self.radius)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.x}, {self.y})'


# noinspection PyTypeChecker
class BezierPoint(Point):
    def __init__(self, x, y, radius, canvas, color, child=False, draw=True):
        super().__init__(x, y, radius, canvas, color, draw=draw, tags=('trails',) if child else ())

    def lerp(self, point, t, child=False):
        return BezierPoint(*((1 - t) * self.coords + point.coords * t),
                           self.radius, self.canvas, 'red', child, self.drawing is not None)

    def draw_lerp(self, point, t):
        if self.drawing is not None:
            self.canvas.create_line(*point.coords, *self.coords, fill='white', width=1, tags=('trails',))
        return self.lerp(point, t, child=True)


class PointGraph:
    def __init__(self, w, h, ms, update=lambda: None):
        self.ms, self.update = ms, update

        self.root = Tk()
        self.root.geometry(f'{w}x{h}')

        self.canvas = Canvas(self.root, width=w, height=h, bg='black')
        self.canvas.pack()

        self.canvas.bind('<Button-1>', lambda e: self.add_point(e.x, e.y))
        self.root.bind('<BackSpace>', lambda e: self.reset())
        self.root.bind('<space>', lambda e: self.pause())

        self.canvas.bind('<ButtonPress-3>', lambda e: self.toggle_pressed())
        self.canvas.bind('<Motion>', lambda e: self.drag(e.x, e.y))
        self.canvas.bind('<ButtonRelease-3>', lambda e: self.toggle_pressed())

        self.points = []
        self.paused = False
        self.right_click_down = False
        self.radius = 3
        self.root.after(1000, self.update())

    def add_point(self, x, y):
        self.points.append(Point(x, y, self.radius, self.canvas, 'red'))

    def toggle_pressed(self):
        self.right_click_down = not self.right_click_down

    def pause(self):
        self.paused = not self.paused

    def reset(self):
        self.points = []
        self.canvas.delete('all')

    def drag(self, x, y):
        if not self.right_click_down:
            return

        for point in self.points:
            if dist(point.coords, (x, y)) < self.radius:
                point.move(x, y)
                return

    def run(self):
        self.root.mainloop()


class BezierGraph(PointGraph):
    def __init__(self, w, h, bezier):
        self.last_trail = None
        self.increment = 0.002
        super().__init__(w, h, 1, self.play)

        self.bezier = bezier
        self.lines = True
        self.t = 0

    def toggle_lines(self):
        self.lines = not self.lines

    def add_point(self, x, y):
        self.points.append(BezierPoint(x, y, self.radius, self.canvas, 'white'))
        self.last_trail = self.points[0].coords
        self.restart()

    def play(self):
        if self.paused or len(self.points) < 2 or self.last_trail is None:
            self.root.after(self.ms, self.play)
            return

        if self.t >= 1:
            self.restart()
        self.canvas.delete('trails')

        nbp = self.bezier(self.points, self.t, self.lines)
        self.canvas.create_line(*self.last_trail, *nbp.coords, fill='white', width=1, tags=('curve',))
        self.last_trail = nbp.coords

        self.t += self.increment
        self.root.after(self.ms, self.play)

    def reset(self):
        self.points = []
        self.canvas.delete('all')
        self.t = 0
        self.last_trail = None

    def restart(self):
        self.last_trail = self.points[0].coords
        self.canvas.delete('curve')
        self.t = 0
