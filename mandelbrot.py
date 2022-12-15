from PIL import Image
from time import time

def mandelbrot(z, c):
    a, b = z
    x0, y0 = c
    return a * a - b * b + x0, 2 * a * b + y0


def magnitude(z):
    a, b = z
    return a * a + b * b


def iterate(c, threshold, rounds):
    z = 0, 0
    for _ in range(rounds):
        z = mandelbrot(z, c)

    return max(0, threshold * threshold - magnitude(z))


def draw_set(width, height, x0, x1, y0, y1, threshold, rounds):
    ws, hs, cs = (x1 - x0) / width, (y1 - y0) / height, 255 / (threshold * threshold)

    img = Image.new('RGB', (width, height), (0, 0, 0))
    for x in range(width):
        x_i = x * ws
        for y in range(height):
            y_i = y * hs
            img.putpixel((x, y), int(cs * iterate((x0 + x_i, y0 - y_i), threshold, rounds)))
    return img


img = draw_set(1920, 1080, -3, 3, )
img.save(f'mandelbrot_{int(time())}.png')
img.show()
