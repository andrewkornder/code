import tkinter

def update(value):
    x = 100 +int(value)
    canvas.delete('all')
    canvas.create_oval(x + 10, 90, x - 10, 110, fill={1:'blue', 2:'red', 3:'green'}[int(choice.get())])

def checkpwd(event):
    if pwd.get() == 'password123':
        root.destroy()

if __name__ == '__main__':
    root = tkinter.Tk()
    root.geometry('500x500')
    canvas = tkinter.Canvas(root, width=200, height=200, bg='white')
    canvas.pack()
    
    lbl = tkinter.Label(root, text='enter password to quit the window')
    hint = tkinter.Label(root, text='hint: may or may not be "password123"')
    lbl.pack()
    hint.pack()
    root.bind('<Return>', checkpwd)
    pwd = tkinter.Entry(root, show='*', width=20)
    pwd.pack()
    
    choice = tkinter.StringVar(root, 1)
    canvas.create_oval(390, 90, 410, 110, fill='blue')
    
    r1 = tkinter.Radiobutton(root, text="red", variable=choice, value=2)
    r2 = tkinter.Radiobutton(root, text="green", variable=choice, value=3)
    r3 = tkinter.Radiobutton(root, text="blue", variable=choice, value=1)
    r1.pack()
    r2.pack()
    r3.pack()
    
    slider = tkinter.Scale(root, from_=-100, to=100, tickinterval=1, length=200, command=update, orient=tkinter.HORIZONTAL)
    slider.pack()
    
    root.mainloop()