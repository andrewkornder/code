g,l,t,p,f=__import__('PIL.Image'),__import__('os'),255/24,r'images',lambda h,s:'\n'.join(''.join('$@B%8&WM#*o-_+~<>;:,"^`. '[-int(sum(sum(pixel[:3])for pixel in block)/(3*s**2)/t)]for block in row)for row in(lambda i:[[[i.getpixel((x+a,y+b))for a in range(s)for b in range(s)]for x in range(0,i.size[0]-s,s)]for y in range(0,i.size[1]-s,s)])(g.Image.open(h)))
while 1:print(f('%s/%s'%(p,input()),int(input())))


# while 1:print(title_font('%s/%s'%(p,input('\n'.join(l.listdir(p))+'\n\nchoose a file: ')),int(input('choose a compression size: '))))