import tkinter
import math


class Camera:
    def __init__(self, x, y, canvas, dim):
        self.x, self.y, self.z = x, y, 0

        self.canvas = canvas
        self.dim = dim
        self.objects = []

    def draw(self):
        self.canvas.delete('all')
        for obj in self.objects:
            for line in obj.lines:
                p1, p2 = line.scale()
                self.canvas.create_line(p1, p2, fill='white')
                print(p1, p2, *line.points(), (self.x, self.y, self.z))


dim = 800
root = tkinter.Tk()
root.geometry(f'{dim}x{dim}')

canvas = tkinter.Canvas(root, width=dim, height=dim, bg='black')
canvas.pack()

global camera
camera = Camera(dim / 2, dim / 2, canvas, dim)


class Line:
    def __init__(self, p1, p2):
        self.x, self.y, self.z = p1
        self.x1, self.y1, self.z1 = p2
        self.lx, self.ly = self.x - self.x1, self.y - self.y1

    def points(self):
        return (self.x, self.y, self.z), (self.x1, self.y1, self.z1)

    def scale(self):
        print('\n\n')
        """
        perceived height = actual height / distance from viewer
        """
        center_x, center_y = (self.x + self.x1) / 2, (self.y - self.y1) / 2
        # distance = math.dist((center_x, center_y), (camera.x, camera.y))
        distance = abs(((self.z + self.z1) / 2) - camera.z) / 100
        if distance < 1:
            return self.points()
        x_length = self.lx / distance
        y_length = self.ly / distance
        print(distance, self.lx, self.ly, x_length, y_length)
        p1 = center_x - x_length, center_y - y_length
        p2 = center_x + x_length, center_y + y_length

        return p1, p2


class Cube:
    multipliers = [
        # front side
        (-1, -1, 1),
        (-1, 1, 1),
        (1, 1, 1),
        (1, -1, 1),
        # back side
        (-1, -1, -1),
        (-1, 1, -1),
        (1, 1, -1),
        (1, -1, -1)
        ]

    def __init__(self, center, size):
        self.front, self.back = self.set_up(center, size)
        self.lines = self.front # + self.back

    def set_up(self, point, size):
        x, y, z = point
        points = [
            (x + i * size, y + j * size, z + k * size)
            for i, j, k in self.multipliers]
        front = [Line(p, points[(i + 1) if i != 3 else 0]) for i, p in enumerate(points[:4])]
        back = [Line(p, points[(i + 1) if i != 3 else 0]) for i, p in enumerate(points[4:])]
        return front, back


def loop():
    camera.draw()
    #root.after(10000, loop)


if __name__ == '__main__':
    camera.objects.append(Cube((400, 400, 200), 50))
    loop()
    root.mainloop()
