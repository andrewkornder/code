import tkinter
from colour import Color

def sunset():
    global sun, sun_y, curr_sky
    canvas.delete(sun)
    sun = canvas.create_oval(30, sun_y, 60, sun_y + 30, fill = '#ffff00')
    sun_y += 2
    if sun_y + 30 > 115:
        return None
    if curr_sky < len(blues) - 1:
        curr_sky += 1
        canvas['bg'] = blues[curr_sky]
    window.after(10, sunset)
    
def create_sky():
    global sun
    greens = list([x.hex_l for x in Color('springgreen').range_to(Color('darkgreen'), 15)])    
    for y in range(120, 201, 10):
        canvas.create_line((0, y), (200, y), width=10, fill=greens[int(y/10) - 12])
    sun = canvas.create_oval(30, sun_y, 60, sun_y + 30, fill = '#ffff00')
    canvas.create_line((200, 200), (200, 0), fill='#ffffff', width = 1)
    sunset()
    
if __name__ == '__main__':
    window = tkinter.Tk()
    window.geometry('200x200')
    
    blues = list([x.hex_l for x in Color('blue').range_to(Color('darkblue'), 15)])
    sun = None
    sun_y = 30
    curr_sky = 0
    
    canvas = tkinter.Canvas(window, width=200, height=200, bg=blues[curr_sky])
    canvas.pack()
    create_sky()
    window.mainloop()