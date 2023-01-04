class Ray:
    def __init__(self, x, y, z, alpha, beta):
        # alpha turns left - right, beta turns up - down
        self.x, self.y, self.z = x, y, z

        # should satisfy sqrt(dx*dx + dy*dy + dz*dz) = 1
        self.dx = 0
        self.dy = 0
        self.dz = 0


    def run(self, step_size=1, total_steps=100):
        dx, dy, dz = self.dx * step_size, self.dy * step_size, self.dz * step_size
        for steps in range(total_steps):
            self.x = self.x + dx
            self.y = self.y + dy
            self.z = self.z + dz


class Object:
    def __init__(self, x, y, z, color):
        self.x, self.y, self.z = x, y, z
        self.polygons = []

    @property
    def coords(self):
        return self.x, self.y, self.z


class Poly:  # should all be triangles
    def __init__(self, a, b, c):
        # a, b, c are all vectors of length 3
        self.a, self.b, self.c = a, b, c

    def collide(self, ray):
        pass


 
class Cube(Object):
    def __init__(self, x, y, z, color, side):
        super().__init__(x, y, z, color)
        self.polygons = [

        ]
