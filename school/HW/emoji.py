import tkinter

def emoji():
    canvas.create_oval((100, 100, 900, 900), fill='#ffdd00')
    canvas.create_line((300, 700, 700, 700), fill='black', width=10)
    canvas.create_oval((330, 330, 410, 470), fill='black')
    canvas.create_oval((670, 330, 590, 470), fill='black')
    
if __name__ == '__main__':
    window = tkinter.Tk()
    window.geometry('1000x1000')
    canvas = tkinter.Canvas(window, width=1000, height=1000, bg='black')
    canvas.pack()
    emoji()
    window.mainloop()