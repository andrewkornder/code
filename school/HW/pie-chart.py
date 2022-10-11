import tkinter
from colour import Color

def chart():
    total = sum(numbers)
    current_start = 0
    for i, n in enumerate(numbers):
        percent = n/total
        degrees = int(360 * percent)
        if i == len(numbers) - 1:
            degrees = 360 - current_start
        canvas.create_arc(200, 200, 800, 800, extent=degrees, start=current_start, fill=all_colors[i], outline='black', style=tkinter.PIESLICE)
        current_start += degrees
        print(current_start)
    
if __name__ == '__main__':
    window = tkinter.Tk()
    window.geometry('1000x1000')
    canvas = tkinter.Canvas(window, width=1000, height=1000, bg='white')
    canvas.pack()
    numbers = list(map(int, input('input numbers for the chart: ').split()))
    all_colors = list([x.hex_l for x in Color('red').range_to(Color('green'), len(numbers))])
    chart()
    window.mainloop()