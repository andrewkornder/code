from tkinter import *
from PIL import Image, ImageTk
import random as r
import math 

def random():
    dim = [1, 1]#input('input dim for image (w x h)\n').split()
    print('generating img')
    if len(dim) == 0:
        dim = [100, 100]
    w = int(dim[0])
    h = int(dim[1])
    new = Image.new("RGB", (w, h), "blue") 
    for col in range(w):
        for row in range(h):
            new.putpixel((col, row),  (r.randint(0, 256), r.randint(0, 256), r.randint(0, 256)))
    new.save('image1.png')
    new.close()


def shapes():
    w, h = 600, 600
    shapes = Image.new("RGB", (w, h), "blue")
    for y in [100, 400]:
        for x in range(w):
            shapes.putpixel((y, x), (255, 0, 0))
            shapes.putpixel((x, y), (0, 255, 0))
    for x in range(w):
        shapes.putpixel((x, x), (255, 255, 255))
        for y in range(h):
            if y<551 and x>49:
                if math.dist((x, y), (100, 500)) < 50:
                    shapes.putpixel((x, y), (255, 0, 0))
    for x in [150, 200]:
        for y in range(150, 200):
            shapes.putpixel((x, y), (255, 255, 0))
            shapes.putpixel((y, x), (255, 255, 0))
    
    #shapes.show()
    shapes.save('image2.png')
    shapes.close()    
    return shapes

#random()
shapes()
root = Tk()
img = PhotoImage(file="image1.png")
img2 = PhotoImage(file = 'image2.png')
image_label = Label(image = img)
image_label.pack()
image_label2 = Label(image = img2)
image_label2.pack()
root.mainloop()
