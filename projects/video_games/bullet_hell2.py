import tkinter

class Weapon:
    def __init__(self, speed, bullets, spread):
        self.speed, self.bullets, self.spread = speed, bullets, spread
    

class Player:
    size = 10
    color = 'red'
    speed = 5
    
    def __init__(self, canvas, x, y):
        self.x, self.y = x, y
        self.dx, self.dy = 0, 0
        self.moveable = False
        self.canvas = canvas
        self.dash_cooldown = True
        
        self.drawing = canvas.create_oval(self.x - self.size, self.y - self.size, self.x + self.size, self.y + self.size,
                                          fill=self.color)
        self.health = 10
    
    def dash(self):
        if self.dash_cooldown:
            print(self.dx)
            self.x += self.dx * 10
            self.y += self.dy * 10
            self.canvas.moveto(self.drawing, self.x, self.y)
            self.canvas.after(3000, self.reset_dash)
        print(5)
        
    def toggle_move(self):
        self.moveable = not self.moveable
        
    def update(self, event):
        sx, sy = self.x - event.y, self.y - event.y
        if sx == sy == 0:
            self.dx, self.dy = 0, 0
            return
        d = -self.speed / (abs(sx) + abs(sy))
        self.dx = d * sx
        self.dy = d * sy
    
    def move(self):
        if self.moveable:
            self.x += self.dx
            self.y += self.dy
            self.canvas.moveto(self.drawing, self.x, self.y)
        self.canvas.after(10, self.move)
    
    def reset_dash(self):
        self.dash_cooldown = True
        

dim = 800
root = tkinter.Tk()
root.geometry(f'{dim}x{dim}')

canvas = tkinter.Canvas(root, width=dim, height=dim)
canvas.pack()

player = Player(canvas, dim // 2, dim // 2)

canvas.bind('<Motion>', player.update)
canvas.bind('<ButtonPress-1>', lambda e: player.toggle_move())
canvas.bind('<ButtonRelease-1>', lambda e: player.toggle_move())

player.move()
root.mainloop()