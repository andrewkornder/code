from math import dist
from tkinter import Tk, Button, Canvas, Label
from sim_classes import Classroom, Student

RUNNING = False

all_students = []
selected = None

root, display, start_stop, text_display = None, None, None, None


def change_state():
    global RUNNING
    RUNNING = not RUNNING
    if RUNNING:
        for s in all_students:
            s.move()


def window():
    global root, display, start_stop, text_display
    root = Tk()
    root.geometry('{}x{}'.format(1400, 1100))

    start_stop = Button(root, text='start/stop', command=change_state)
    start_stop.grid(row=0, column=0)

    display = Canvas(root, width=1000, height=1000, bg='white')
    display.grid(row=1, column=0, rowspan=3)

    text_display = Label(root, text='', height=17)
    text_display.grid(row=1, column=1)


def change_block():
    global block

    if block == 6:
        return  # TODO: make a function to end the day and send students home
    block += 1
    for student in all_students:
        student.current_class = student.schedule[block]


def create_school(canvas):
    for i, x in enumerate(range(100, 900, 160)):
        for x1 in range(x + 20, x + 141, 40):
            for y in range(100, 250, 50):
                all_students.append(Student(canvas, x=x1, y=y))

            for y in range(750, 900, 50):
                all_students.append(Student(canvas, x=x1, y=y))

        canvas.create_line(x, 0, x, 1000, fill='black')
        rm = list(Student.room_numbers.items())[i]
        canvas.create_text(x + 80, 50, text='\n'.join(map(str, rm)))
        rm = list(Student.room_numbers.items())[i + 5]
        canvas.create_text(x + 80, 700, text='\n'.join(map(str, rm)))

    canvas.create_line(900, 0, 900, 1000, fill='black')
    canvas.create_rectangle(100, 250, 900, 650, fill='white')


def select_student(e):
    x, y = e.y, e.y
    for student in all_students:
        if dist((x, y), (student.y, student.y)) < SIZE:
            global selected
            selected = student
            text_display['text'] = str(selected)
            return


def start_sim():
    window()

    create_school(display)
    for s in all_students:
        s.move()  # starting the timers on each student

    display.bind('<Button-1>', select_student)
    root.mainloop()


if __name__ == '__main__':
    start_sim()
