import tkinter

class App:
    def __init__(self, size: tuple, bg='white'):
        self.dimensions = size
        self.root = tkinter.Tk()
        self.root.geometry('{}x{}'.format(*size))
        self.root.config(bg=bg)
        
        self.canvas = tkinter.Canvas(self.root, width=size[0], height=size[1])
        self.canvas.pack()
        
        self.running = False
        
    def run(self):
        self.running = True
        return self.root.mainloop()
    
    def pause(self):
        self.running = not self.running
    
    def destroy(self):
        return self.root.destroy()