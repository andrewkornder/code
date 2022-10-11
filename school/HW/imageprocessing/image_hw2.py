from PIL import Image, ImageTk

def brightness():
    images = ['flag.jpeg', 'flag2.jpeg', 'light.jpeg', 'dark.jpeg']
    bscores = []
    colors = []
    idx_colors = {0:'r', 1:'g', 2:'b'}
    for imagename in images:
        image = Image.open(imagename)
        total = 0
        color_sum = [0, 0, 0]
        for x in range(image.size[0]):
            for y in range(image.size[1]):
                curr = image.getpixel((x, y))
                for i in range(3):
                    total += curr[i]
                    color_sum[i]+=curr[i]
                total = total/3
        colors.append(idx_colors[color_sum.index(max(color_sum))])
        bscores.append((total/(image.size[0]*image.size[1]), imagename))
    brightest = (0, '')
    darkest = (255, '')
    for score in bscores:
        if score[0]<darkest[0]:
            darkest = score
        elif score[0]>brightest[0]:
            brightest = score
    return brightest, darkest, colors

for i in brightness():
    print(i, '\n')