from random import choice
from math import dist
from simCC_app import App

seats = []
SIZE = 15
POPULATION = 5
FIRST_NAMES = open('../first_names.txt').read().split('\n')
LAST_NAMES = open('../last_names.txt').read().split('\n')
COLORS = [
    'red',
    'blue',
    'green',
    'purple',
    'orange',
    'grey'
]


class Student:
    speed, size = 5, 12

    @staticmethod
    def get_name():
        return '%s %s' % (choice(FIRST_NAMES), choice(LAST_NAMES).capitalize())

    def __init__(self, display, x, y, classroom):
        self.name = self.get_name()
        self.x, self.y = x, y
        self.dx, self.dy = 0, 0
        self.destination = None
        self.classroom = classroom
        self.display = display
        self.color = choice(COLORS)
        self.drawing = display.create_oval(*self.get_oval(), fill=self.color)

        self.phase = 0

    def choose_destination(self):
        if self.phase == 1:
            return self.classroom.door_coords[-1]
        return self.destination.door_coords[-1]

    def get_oval(self):
        return self.x - self.size, self.y - self.size, self.x + self.size, self.y + self.size

    def get_direction(self):
        x1, y1 = self.choose_destination()
        sx, sy = self.x - x1, self.y - y1
        d = -self.speed / (abs(sy) + abs(sx))
        x_dist, y_dist = d * sx, d * sy
        return x_dist, y_dist

    def arrived(self, a, b, c, d):
        return (a < self.x < c) and (b < self.y < d)

    def move(self):
        if not self.phase:  # meaning the student is stationary at a 'desk'
            return

        if self.arrived(*self.destination.door_coords[:-1]):
            self.sit_down(self.destination)

        elif self.arrived(*self.classroom.door_coords[:-1]):
            self.phase = 2

        self.dx, self.dy = self.get_direction()
        self.x += self.dx
        self.y += self.dy

        """for s in all_students:
            if s is self:
                continue
            if dist((self.x, self.y), (s.x, s.y)) < (Student.size * 2):
                self.x -= self.dx
                self.y -= self.dy
                self.shove(s)"""

        self.display.delete(self.drawing)
        self.drawing = self.display.create_oval(*self.get_oval(), fill=self.color)

    def sit_down(self, classroom):
        if classroom.full:
            self.destination = choice(self.get_classes())
            return

        r = classroom.next_desk()
        if r is False:
            self.destination = choice(self.get_classes())
            return

        self.x, self.y = r
        self.phase = 0
        self.classroom = classroom

    def move_to(self):
        self.classroom.leave((self.x, self.y))
        self.phase = 1
        self.destination = choice([a for a in all_rooms if not a.full])

    def get_classes(self):
        classes = [a for a in all_rooms if not a.full and a is not self.classroom]
        if not classes:
            classes.append(self.classroom)  # will only allow a person to stay in a classroom if none other are open
        return classes

    def shove(self, other):
        # self is above or below to other
        if abs(self.x - other.y) < 5:
            self.dy *= -1
        if abs(self.y - other.y) < 5:
            self.dx *= -1

        self.x += self.dx
        self.y += self.dy


class Room:
    height = 200
    width = 100

    door_width = 75
    door_depth = 20

    def __init__(self, display, x, y, size, subject, room_number):
        self.subject = subject
        self.number = room_number
        self.display = display
        self.x, self.y = x, y

        x += 68
        y += self.height

        a, b, c, d = x - self.door_width, y - self.door_depth, x + self.door_width, y + self.door_depth
        if y > 500:
            b, d = b - self.height * 2, d - self.height * 2
        self.door_coords = [a, b, c, d]
        display.create_rectangle(x - self.width, y - self.height * 2, x + self.width, y)
        display.create_rectangle(*self.door_coords, fill='white')

        self.door_coords.append(((a + c) / 2, (b + d) / 2))
        self.capacity = 0
        self.row_size = 5

        self.full = True
        self.locations = {}

        for i in range(size):
            mult = Student.size * 2 + 10
            a = mult * (i // self.row_size)
            b = mult * (i % self.row_size)
            self.locations[(self.x + b, self.y + a)] = True

    def next_desk(self):
        for loc, usage in self.locations.items():
            if not usage:
                self.locations[loc] = True
                return loc
        self.full = True
        return False

    def leave(self, key):
        self.full = False
        self.locations[key] = False


window = App()
subjects = [
    [('math', 121),
     ('science', 122),
     ('english', 123),
     ('history', 124)],
    [('spanish', 221),
     ('lunch', 222),
     ('adv py', 223),
     ('study', 234)]
]
total_students = 80

all_rooms, all_students = [], []


def draw_map():
    global all_rooms, all_students
    for r, row in enumerate(subjects):
        y = 200 + r * 600

        for c, (sub, rn) in enumerate(row):
            x = 200 * c + 100
            new_class = Room(window.canvas, x, y, 10, sub, rn)
            all_rooms.append(new_class)
            loc = list(new_class.locations.keys())
            for s in range(10):
                nx, ny = loc[s]
                all_students.append(Student(window.canvas, nx, ny, new_class))


def on_click(event):
    x, y = event.y, event.y
    for s in all_students:
        if dist((x, y), (s.y, s.y)) < Student.size:
            print(s.name)
            return


def change_block():
    for s in all_students:
        s.move_to()
    window.root.after(10000, change_block)


def animate():
    for s in all_students:
        s.move()

    window.root.after(10, animate)


window.canvas.bind('<Button-1>', on_click)
animate()
draw_map()
window.root.after(100, change_block)
window.run()
