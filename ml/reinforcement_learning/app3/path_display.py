from constants import *

from scipy.interpolate import BSpline


class PathDisplay:
    @staticmethod
    def circle(x, y, r):
        return x - r, y - r, x + r, y + r

    def __init__(self, points, canvas, style='linear', definition=100, palette=None, radius=0.05):
        self.points = points if style == 'linear' else (self.b_spline(points, definition)
                                                        if style == 'interpolated' else [])
        self.length = len(self.points)
        self.segments = self.length - 1
        self.canvas = canvas

        if style == 'interpolated':
            self.palette = [Constants.walk_color if palette is None else palette] * self.segments
        elif style == 'linear':
            if palette is None or len(palette) != self.segments:
                self.palette = [Constants.walk_color] * self.segments
            else:
                self.palette = palette

        self.last = self.points[0]
        self.radius = int(radius * Constants.size)

        self.index = 1
        self.ms = int(1000 * (Constants.walk_time / self.length) - 1)
        self.drawing = canvas.create_oval(*self.circle(*self.last, self.radius), fill=Constants.walk_color, tags=('path',))
        self.iterate()

    @staticmethod
    def b_spline(points, n):
        degree, sign = 0, [False, False]
        for i, point in enumerate(points[1:]):
            new_sign = [a >= 0 for a in points[i] - point]
            if new_sign != sign:
                degree += 1
            sign = new_sign

        count = points.shape[0]

        degree = np.clip(degree, 1, count - 1)
        kv = np.clip(np.arange(count + degree + 1) - degree, 0, count - degree)

        # noinspection PyTypeChecker
        return BSpline(kv, points, degree)(np.linspace(0, count - degree, n))

    def iterate(self):
        x, y = self.points[self.index]
        self.canvas.create_line(*self.last, x, y, fill=self.palette[self.index - 1], tags=('path',))
        self.canvas.moveto(self.drawing, x - self.radius, y - self.radius)
        self.last = x, y

        self.index += 1
        if self.index < self.length:
            self.canvas.after(self.ms, self.iterate)
