from tkinter import *
from PIL import Image, ImageTk

def avg(img):
    avgc = [(0, 0, 0)*2]
    totals = [[0, 0, 0], [0, 0, 0]]
    hlen = [int(img.size[1]/2)]
    for h in range(img.size[1]):
        for w in range(img.size[0]):
            pixel = img.getpixel((w, h))
            if h<img.size[1]/2:
                for i in range(3):
                    totals[0][i] += pixel[i]
            else:
                for i in range(3):
                    totals[1][i] += pixel[i]                
    totals = [[int(i/(img.size[0]*img.size[1]/2)) for i in c] for c in totals]
    avgc = [tuple(i) for i in totals]
    new = Image.new("RGB", (img.size[0], img.size[1]), avgc[0])
    for h in range(int(new.size[1]/2), new.size[1]):
        for w in range(new.size[0]):
            pixel = new.putpixel((w, h), avgc[1])
    new.save('image3.png')
    new.close()
    
    
    
file = 'flag.jpeg'
avg(Image.open(file))
root = Tk()
img = PhotoImage(file="image3.png")
image_label = Label(image = img)
image_label.pack()
root.mainloop()