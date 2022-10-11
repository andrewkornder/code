from random import randint, choice
from math import dist
from tkinter import Tk, Button, Canvas, Label

SIZE = 15
RUNNING = True
POPULATION = 5
FIRST_NAMES = open('first_names.txt').read().split('\n')
LAST_NAMES = open('last_names.txt').read().split('\n')
COLORS = [
    'red',
    'blue',
    'green',
    'purple',
    'orange'
]


class App:
    def __init__(self, objects=None):
        self.running = False
        self.frame_rate = 10

        self.root = Tk()
        self.root.geometry('{}x{}'.format(1400, 1100))

        self.start_stop = Button(self.root, text='start/stop', command=self.change_block)
        self.start_stop.grid(row=0, column=0)

        self.canvas = Canvas(self.root, width=1000, height=1000, bg='white')
        self.canvas.bind('<Button-1>', self.on_click)
        self.canvas.grid(row=1, column=0, rowspan=3)

        self.text_display = Label(self.root, text='', height=17)
        self.text_display.grid(row=1, column=1)

        self.objects = objects if objects else []
        self.refresh_frame()

    def on_click(self, event):
        x, y = event.y, event.y
        for c in self.objects:
            for s in c.students:
                if dist((x, y), (s.y, s.y)) < Student.size:
                    print(s.get_info())
                    return

    def pause(self):
        self.running = not self.running

    def refresh_frame(self):
        if not self.running:
            for obj in self.objects:
                obj.update()
        self.root.after(self.frame_rate, self.refresh_frame)

    def run(self):
        self.root.mainloop()

    def change_block(self):
        for obj in self.objects:
            obj.change_block(self.objects)
            
    def full_refresh(self):
        for obj in self.objects:
            obj.redraw()

class Classroom:
    def __init__(self, display, subject, room, x, y):
        self.display = display
        self.color = choice(COLORS)

        self.subject = subject
        self.room = room
        self.x, self.y = x, y
        self.bounds = 180, 95

        self.students = []
        self.drawings = []

        self.class_size, self.row_size = 10, 5
        self.populate(self.class_size)

    def populate(self, count):
        for s in range(count):
            new_student = Student(self)
            drawing = self.display.create_oval(
                *new_student.get_circle(),
                fill=self.color
            )
            self.students.append(new_student)
            self.drawings.append(drawing)

    def get_location(self):
        mult = Student.size * 2 + 10
        y = mult * (len(self.students) // self.row_size)
        x = mult * (len(self.students) % self.row_size)
        return x + self.x, y + self.y

    def update(self):
        for student, drawing in zip(self.students[:], self.drawings):
            student.y += student.dx
            student.y += student.dy

            self.display.move(drawing, student.dx, student.dy)
            
            if student.check_destination():
                self.display.delete(drawing)
                self.drawings.remove(drawing)
                self.students.remove(student)
                student.classroom.students.append(student)
                student.dx, student.dy = 0, 0

    def change_block(self, classrooms):
        print(self.students)
        for student, drawing in zip(self.students[:], self.drawings[:]):

            new_class = choice(classrooms)
            while new_class is self:
                new_class = choice(classrooms)  # avoiding a division by zero error

            student.move_to(new_class)
    
    def redraw(self):
        for student, drawing in zip(self.students, self.drawings[:]):
            self.display.delete(drawing)
            self.drawings.remove(drawing)
            self.drawings.append(self.display.create_oval(
                *student.get_circle(),
                fill=self.color
            ))        

class Student:
    size = 15
    speed = 2

    @staticmethod
    def get_name():
        return f'{choice(FIRST_NAMES)} {choice(LAST_NAMES).capitalize()}'

    def __init__(self, classroom):
        self.classroom = classroom
        self.name = self.get_name()

        self.x, self.y = classroom.get_location()
        self.dx, self.dy = 0, 0

    def get_info(self):
        return f'{self.name}: in {self.classroom.subject} class, room {self.classroom.room}'

    def get_circle(self):
        x, y = self.x - self.size, self.y - self.size
        x1, y1 = self.x + self.size, self.y + self.size
        return x, y, x1, y1

    def move_to(self, classroom):
        self.classroom = classroom
        sx, sy = self.x - classroom.y, self.y - classroom.y
        if sx and sy:
            s = self.speed / (abs(sx) + abs(sy))
            self.dx, self.dy = -s * sx, -s * sy
            return
        self.dx, self.dy = 0, 0
    
    def check_destination(self):
        bx, by = self.classroom.bounds
        cx, cy = self.classroom.y, self.classroom.y
        
        return (cx - 20 < self.x < cx + bx and cy - by < self.y < cy + by)

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

def draw_map():
    for r, row in enumerate(subjects):
        y = 200 + 600 * r
        for c, (subject, room_no) in enumerate(row):
            x = 100 + 200 * c
            window.canvas.create_line(x - 20, 1000, x - 20, 0)
            window.objects.append(Classroom(window.canvas, subject, room_no, x, y))
    window.canvas.create_line(880, 1000, 880, 0)
    window.canvas.create_rectangle(80, 290, 880, 750, fill='white')
    window.full_refresh()

draw_map()
window.run()
