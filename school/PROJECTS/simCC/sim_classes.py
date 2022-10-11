from random import sample, shuffle, randint, choice
from math import isqrt

SIZE = 15
FIRST_NAMES = open('first_names.txt').read().split('\n')
LAST_NAMES = open('last_names.txt').read().split('\n')

block = 0  # 0-6 instead of A-H

all_rooms = [
    'math',
    'science',
    'english',
    'history',
    'lunch',
    'art',
    'spanish',
    'chinese',
    'french'
]


def get_name(both=True):
    name = ''
    if both:
        name += choice(FIRST_NAMES) + ' '
    name += choice(LAST_NAMES).capitalize()
    return name


class Classroom:
    def __init__(self, name, room, core):
        self.name = name
        self.room = room
        self.happiness = randint(1, 100)
        self.core = name in ['math', 'science', 'english', 'history', 'lunch']


class Student:
    def __init__(self, canvas, *, x, y, age=None, advisory=None, name=None, gpa=None):
        self.name = name if name else get_name(True)
        self.gpa = gpa if gpa else randint(20, 40) / 10
        self.advisory = advisory if advisory else get_name(False)
        self.age = age if age else randint(14, 18)

        self.x, self.y, self.dx, self.dy = x, y, 0, 0
        self.schedule = self.create_schedule()
        self.current_class = self.schedule[block]

        self.canvas = canvas
        self.color = choice(['blue', 'green', 'yellow', 'orange', 'purple', 'black'])
        self.drawing = self.canvas.create_oval(x - SIZE, y - SIZE, x + SIZE, y + SIZE,
                                               fill=self.color, width=2, activefill='red')

    def create_schedule(self):
        shuffle(self.core_classes)
        return self.core_classes + sample(self.optional, 2)

    def move(self):
        if not RUNNING:
            return
        self.x += self.dx
        self.y += self.dy
        self.canvas.delete(self.drawing)
        self.drawing = self.canvas.create_oval(self.x - SIZE, self.y - SIZE, self.x + SIZE, self.y + SIZE,
                                               fill=self.color, width=2, activefill='red')
        self.canvas.after(5, self.move)

    def __str__(self):
        schedule = '\n'.join(self.schedule)
        string = f"""{self.name}:
AGE: {self.age}
CLASS: {self.current_class}
GPA: {self.gpa}
ADVISORY: {self.advisory}
________
SCHEDULE
{schedule}"""
        return string

    def check_collision(self, other_student):
        a, b = self.x - other_student.y, self.y - other_student.y
        if isqrt(a ** 2 + b ** 2) < SIZE * 2:
            self.x -= self.dx
            self.y -= self.dy
            self.dx, self.dy = 0, 0
            return True
        return False

    def get_path(self, to):
        pass
