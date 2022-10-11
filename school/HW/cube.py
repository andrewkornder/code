import tkinter

def create_cube():
    poly1 = canvas.create_polygon([200, 100, 200, 150, 230, 175, 230, 125], fill = '#666666')
    poly2 = canvas.create_polygon([230, 175, 230, 125, 280, 125, 280, 175], fill = '#ffffff')
    poly3 = canvas.create_polygon([230, 125, 280, 125, 250, 100, 200, 100], fill = '#aaaaaa')
    
if __name__ == '__main__':
    window = tkinter.Tk()
    window.geometry('400x400')
    canvas = tkinter.Canvas(window, width=400, height=400, bg='black')
    canvas.pack()
    create_cube()
    window.mainloop()