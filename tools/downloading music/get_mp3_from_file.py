from threading import Thread
from os import system

f = 'links.txt'
def t(l): system(f'youtube-dl --extract-audio --audio-format mp3 --embed-thumbnail -o "%(title)s.mp3"{l}')
for l in open(f).read().split('\n'): Thread(target=t,args=(l,)).start()