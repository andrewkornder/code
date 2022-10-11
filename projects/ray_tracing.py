import math
import random as r
import numpy as np

objects = []


class Ray:
    def __init__(self, x=0, y=0, z=0, ah=0, av=0, bounces=1, step=10):
        """
        sends an angle out from the camera at the angle given.

        :param x: the starting x
        :param y: the starting y
        :param ah: right-left / horizontal angle
        :param av: up-down / vertical angle
        :param bounces: the amount of bounces before it returns the color
        :param step: the speed it moves, slower speed will take more computation, but will be more accurate
        """

        self.bounces = bounces
        self.x, self.y, self.z = x, y, z
        self.dx, self.dy, self.dz = self.calc_delta(ah, av, step)
        self.color = (0, 0, 0)

    def calculate(self):
        while not self.collide():  # until it hits an object
            self.x += self.dx
            self.y += self.dy
            self.z += self.dz

        return self.color

    def collide(self):
        for obj in objects:  # assuming all cubes for now
            if not (-obj.half < obj.y - self.x < obj.half):
                continue
            if not (-obj.half < obj.y - self.y < obj.half):
                continue
            if -obj.half < obj.y - self.x < obj.half:
                self.color = obj.color

    @staticmethod
    def calc_delta(ah, av, step):
        dx = math.sin(ah) * step
        dy = math.sin(av) * step
        dz = math.cos(ah) * step

        return dx, dy, dz

    def coords(self):
        return self.x, self.y, self.z


class Cube:
    def coords(self):
        return self.x, self.y, self.z

    def __init__(self, x, y, z, size):
        self.x, self.y, self.z = x, y, z
        self.size = size
        self.half = size / 2
        self.color = tuple([r.randint(0, 255) for _ in range(3)])


def generate():
    matrix = np.empty((10, 10), dtype=object)
    matrix[:] = 1
    matrix[1:-1, 1:-1] = 0

    done = []
    for _ in range(15):
        x, y = r.randint(1, 8), r.randint(1, 8)
        while (x, y) in done:
            x, y = r.randint(1, 8), r.randint(1, 8)
        matrix[x, y] = 1
    return matrix


def window():
    board = generate()
    board[1,1] = 2

class Player:
    def __init__(self, x, y, z, board, root, canvas):
        self.x, self.y, self.z, self.board = x, y, z, board
        self.root = root
        self.canvas = canvas
        
    def get_vision(self):
        for ah in range(180):
            for av in range(180):
                r = Ray(self.x, self.y, self.z, ah, av)
                self.canvas.create_line(self.
        
