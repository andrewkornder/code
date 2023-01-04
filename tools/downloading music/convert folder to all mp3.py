import os
from moviepy.editor import *

root = r'C:\Users\Administrator\OneDrive\Desktop\other\music'
folder = r'C:\Users\Administrator\OneDrive\Desktop\other\music'
for file in os.listdir(folder):
    if file[-4:] == '.mp4':
        print(file)
        name = file[:-4]
        video = VideoFileClip(f'{folder}\\{file}')
        video.audio.write_audiofile(os.path.join(f'{root}\\{name}.mp3'))
