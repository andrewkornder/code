#!/usr/bin/python
#img_processing.py
__author__ = "Andrew Kornder"
__version__ = '1.0'

'''takes an image and user input to create different versions of said image'''

import date_time_file_name
from PIL import Image
import random as r

def highest_pixel(img1):
    img = Image.new("RGB", img1.size, (255, 255, 255))
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            img.putpixel((x, y), tuple([c if c == max(img1.getpixel((x, y))) else 0 for c in img1.getpixel((x, y))]))
    return img

def spot_diff(img1, img2):
    '''
    returns an image made of all the pixels which were not found in both images
    
    :param img1: the first image which the other image is compared to
    :param img2: the image to be compared
    :return: a new image of all the differing pixels
    '''
    
    img = Image.new("RGB", img1.size, (255, 255, 255))
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            curr = img1.getpixel((x, y))
            if curr != img2.getpixel((x, y)):
                img.putpixel((x, y), curr)
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            curr = img2.getpixel((x, y))
            if curr != img1.getpixel((x, y)):
                img.putpixel((x, y), curr)
    return img  


def inversion(image_obj):
    '''
    returns an image where all the pixels had the color values inverted
    
    :param image_obj: the Image object to be altered
    :return: a new image of all the new color values
    '''
    
    img = Image.new("RGB", image_obj.size)
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            img.putpixel((x, y), tuple([255-p for p in image_obj.getpixel((x, y))]))
    return img

def pixelate(old, amt):
    if amt == '':
        amt = 20
    else:
        amt = int(amt)
    img = Image.new("RGB", old.size)
    for x in range(1, img.size[0], amt):
        for y in range(1, img.size[1], amt):
            #print(x, y)
            total = [0, 0, 0]
            for a in range(amt):
                for b in range(amt):
                    for c in range(3):
                        total[c] += old.getpixel((x-a, y-b))[c]
            rgb = tuple([int(t/(amt**2)) for t in total])
            for a in range(amt):
                for b in range(amt):
                    img.putpixel((x-a, y-b), rgb)
    return img

def shrink(old, ratio):
    '''
    returns a smaller version of the given image
    
    :param old: the old image which will be shrunk
    :param ratio: the given size/ratio for the image to the image to be created
    :return: a smaller version of the given image
    '''
    
    if ratio != '':
        ratio = [int(r) for r in ratio.split(' ')]
    else:
        ratio = [int(p) for p in [old.size[0]/2, old.size[1]/2]]
    newW, newH = ratio[0], ratio[1]
    img = Image.new("RGB", (newW, newH), (0, 0, 0))
    r = int(old.size[0]/newW)
    r2 = int(old.size[1]/newH)
    #print(r, r2)
    for x in range(0, newW):
        for y in range(0, newH):
            curr, rgb = [old.getpixel(((x*r)+k, (y*r2)+j)) for k in range(r) for j in range(r2)], [0, 0, 0]
            #print(curr)
            for c in curr:
                for t in range(3):
                    rgb[t] += c[t]
            rgb = [int(u/len(curr)) for u in rgb]
            img.putpixel((x, y), tuple(rgb))
    return img   

def edge_detection(old):
    '''
    returns a version of the given image with only an outline
    
    :param old: the image which will be changed
    :return: a line-art version of the given image
    '''
    
    img, o = Image.new("RGB", old.size, (0, 0, 0)), black_white(old)
    for x in range(1, img.size[0]-1):
        for y in range(1, img.size[1]-1):
            for p in [(x+a, y+b) for a in range(-1, 1) for b in range(-1, 1)]:
                if o.getpixel((x, y)) != o.getpixel(p):
                    img.putpixel(p, (255, 255, 255))
                    #img.putpixel((x, y), (127, 127, 127))
                    break
    return img
    
def lighten_darken(image_obj, change):
    '''
    returns a smaller version of the given image
    
    :param old: the old image which will be shrunk
    :param ratio: the given size/ratio for the image to the image to be created
    :return: a smaller version of the given image
    '''
    
    img, change = Image.new("RGB", image_obj.size), int(change)
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            curr = [p-change for p in image_obj.getpixel((x, y))]
            img.putpixel((x, y), tuple(curr))
    return img

def grayscale(image_obj):
    '''
    returns a grayscale version of the image
    
    :param image_obj: the image to be filtered
    :return: an image with only gray pixels of the original image
    '''
    
    img = Image.new("RGB", image_obj.size)
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            curr = int(sum(image_obj.getpixel((x, y)))/3)
            img.putpixel((x, y), (curr, curr, curr))
    return img
def border(old, size):
    '''
    returns a grayscale border around an image
    
    :param old: the image to be adjusted
    :return: an image with only gray pixels around the border of the image
    '''
    
    if size == '':
        size = 15
    else:
        size = int(size)
    img = Image.new("RGB", old.size)
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            rgb = int(sum(list(old.getpixel((x, y))))/3)
            if x <= size or x >= img.size[0]-size:
                img.putpixel((x, y), (rgb, rgb, rgb))
            elif y <= size or y  >= img.size[1] - size:
                img.putpixel((x, y), (rgb, rgb, rgb))
            else:
                img.putpixel((x, y), old.getpixel((x, y)))
    return img

def black_white(image_obj):
    '''
    returns a black and white image of the original
    
    :param image_obj: the image to be transformed into black and white
    :return: a black and white image
    '''
    
    img = Image.new("RGB", image_obj.size)
    avg = sum([image_obj.getpixel((x, y))[0] for x in range(img.size[0]) for y in range(img.size[1])])/(img.size[0]*img.size[1])
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            curr = image_obj.getpixel((x, y))[0]
            if curr>avg:
                img.putpixel((x, y), (0, 0, 0))
            else:
                img.putpixel((x, y), (255, 255, 255))
    return img
def block(r, i, x, y):
    p = [[i.getpixel((x+k, y+j)), (x+k, y+j)] for k in range(r) for j in range(r)]
    return p

def remove_edges(img):
    edges = edge_detection(img)
    new = Image.new('RGB', img.size)
    
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            if edges.getpixel((x, y)) == (255, 255, 255):
                new.putpixel((x, y), (0, 0, 0))
            else:
                new.putpixel((x, y), img.getpixel((x, y)))
            '''if edges.getpixel((x, y)) == (255, 255, 255) and y != img.size[1] and x != img.size[0]:
                above, below = img.getpixel((x, y - 1)), img.getpixel((x, y + 1))
                right, left = img.getpixel((x + 1, y)), img.getpixel((x - 1, y))
                totals = []
                for close in [above, below, right, left]:
                    avg = sum(close)/3
                    #print(close)
                    if avg > 50 and avg < 205:
                        totals.colors(close)
                        print('appended')
                newpix = [0, 0, 0]
                for rgb in totals:
                    for index in range(3):
                        newpix[index] += int(rgb[index]/len(totals))
                print(newpix)
                if not len(totals):
                    new.putpixel((x, y), img.getpixel((x, y)))  
                else:
                    new.putpixel((x, y), tuple(newpix))
            else:
                new.putpixel((x, y), img.getpixel((x, y)))'''
    new.show()
    edges.show()
    

def noise(o, iS):
    if iS == '':
        s = 2
    else:
        s = int(iS)
    img = Image.new("RGB", o.size, (0, 0, 0))
    for x in range(s, img.size[0], s):
        for y in range(s, img.size[1], s):
            rc = r.randint(0, 50)
            for a in range(s):
                for b in range(s):
                    img.putpixel((x-a, y-b), tuple([p + rc for p in o.getpixel((x-a, y-b))]))
    return img

def noise2(o):
    divideby = str(min(o.size))
    edges = shrink(inversion(black_white(o)), divideby+' '+divideby)
    img = Image.new("RGB", edges.size)
    b = False
    '''p, nx, ny = [], 0, 0
    s = 5
    t = int(img.size[0]/s) - s
    for z in range(0, t, s):
        color = r.randint(0, 50)
        for a in range(0, t, s):
            #print(z, a)
            curr = [[o.getpixel((z+k, a+j)), (z+k, a+j)] for k in range(s) for j in range(s)]
            for c in curr:
                img.putpixel(c[1], tuple([d + color for d in c[0]]))
        #img.show()'''
    for y in range(img.size[0]-1):
        rgb = o.getpixel((0, 0))
        cc = r.randint(-5, 10)
        for x in range(img.size[0]-1):
            n = edges.getpixel((x+1, y))
            c = edges.getpixel((x, y))
            if c != n:
                if c == edges.getpixel((0, 0)):
                    rgb = tuple([p-50 for p in o.getpixel((x+1, y))])
                    b = True
                else:
                    rgb = tuple([p-50 for p in o.getpixel((x, y))])
                    b = False
            else:
                if b:
                    rgb = o.getpixel((x+1, y))
                else:
                    rgb = tuple([p+r.randint(0, 50)+cc if ind < 3 else p+r.randint(0, 1)+cc for ind, p in enumerate(img.getpixel((x+1, y)))])
                    b = False
            img.putpixel((x, y), rgb)
    return img

def rgbfilter(image_obj, r, g, b):
    '''
    creates an image with limits on the red, green and blue values
    
    :param image_obj: the image which will be used as a starting point
    :param r: the limit on the red values
    :param g: the limit on the green values
    :param b: the limit on the blue values
    :return: a new version with the limits applied to the values
    '''    
    
    filters, img = [int(x) if x != '' else 100 for x in [r, g, b]], Image.new("RGB", image_obj.size)
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            curr = [x if x<filters[p] else filters[p] for p, x in enumerate(image_obj.getpixel((x, y)))]
            img.putpixel((x, y), tuple(curr))
    return img  

def save(image):
    time_stamped_name = date_time_file_name.file_name()
    image.save(time_stamped_name)


def show(image):
    image.show()

if __name__ == '__main__':
    remove_edges(Image.open('images/owl.jpg'))