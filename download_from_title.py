from youtube_search import YoutubeSearch as Search
from os import system, listdir, rename, remove, path
from os import name as operating_sys
from tkinter import Tk, Canvas, Entry, END, NW
from requests import get
from PIL import Image, ImageTk
from threading import Thread
from yt_dlp import YoutubeDL
from shutil import move
import eyed3
from eyed3.id3.frames import ImageFrame


class Downloader:
    def __init__(self, k=None, w=1200, h=800, langs='en,jp',
                 file='to_download', destination='C:/Users/Administrator/OneDrive/Desktop/folders/music/'):
        self.i = 0
        self.queries = open(file, encoding='UTF-8').read().split('\n')
        if k:
            self.queries = self.queries[:k]
        self.langs = langs.split(',')

        self.w, self.h = w, h - 100
        self.length = 3
        self.iw, self.ih = self.w * 3 // 10, (self.h - 50) // self.length

        self.data = {}
        self.current = {}
        self.images = {}
        self.destination = destination.replace('~', path.expanduser('~'))

        self.font = ('Niagara Bold', 10)

        self.root = Tk()
        self.root.geometry(f'{self.w}x{h}')

        self.canvas = Canvas(self.root, width=self.w, height=self.h)
        self.canvas.grid(row=0, column=0)

        self.input = Entry(self.root)
        self.input.grid(row=1, column=0)

        self.canvas.bind('<ButtonRelease-1>', self.select)
        self.canvas.bind('<ButtonPress-3>', self.back)
        self.root.bind('<Return>', self.enter)

    def load_next(self):
        if self.i == len(self.queries):
            self.root.destroy()
            self.download_all()
            return

        self.canvas.delete('all')

        self.current = Search(self.queries[self.i], max_results=self.length).to_dict()

        self.canvas.create_text(self.w / 2, self.ih * self.length + 25, text=self.queries[self.i], font=self.font)

        self.images[self.i] = []
        for j, video in enumerate(self.current):
            name = f'./temp/{video["id"]}.jpg'

            open(name, 'wb').write(get(video['thumbnails'][0]).content)

            im = ImageTk.PhotoImage(Image.open(name).resize((self.iw, self.ih)), master=self.root)
            self.images[self.i].append(im)

            ic = self.w - self.iw, self.ih * j
            self.canvas.create_image(*ic, anchor=NW, image=self.images[self.i][-1])
            self.canvas.create_text(ic[0] / 2, (j + 0.5) * self.ih, font=self.font,
                                    text=f"[{video['duration']}] \"{video['title']}\" - {video['channel']}")

    def enter(self, _):
        self.queries[self.i] = self.input.get()
        self.input.delete(0, END)
        self.load_next()

    def back(self, _):
        self.i -= 1

    def select(self, e):
        if e.y > self.length * self.ih:
            return

        a = self.current[e.y // 250]
        self.data[self.i] = a['id'], a['title'], a['channel']

        self.i += 1
        self.load_next()

    def download_all(self):  # TODO: add id to end of filename, and check if file[-12:-4] is in [ids]
        # TODO: then rewrite all the code to be less shitty & cleanup imports and funcs

        ids, songs, artists = list(zip(*self.data.values()))

        songs = list(map(sanitize, songs))
        print('\n'.join([''] + songs), '\n')

        opts = {
            'audio-format': 'mp3',
            'extract-audio': True,
            'write-subs': True,
            'sub-langs': 'en,jp,ja',
            'write-thumbnail': True,
            'no-check-certificate': True,
            'add-metadata': True,
            'ffmpeg-location': '~/Downloads/',
            'o': f'{self.destination}/%(id)s.mp3',
            'postprocessors': [{  # Extract audio using ffmpeg
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }]
        }
        with YoutubeDL(opts) as yt:
            # yt.download(ids)
            threads = [Thread(target=lambda x: yt.download(x), args=(id,)) for id in ids]

        [t.start() for t in threads]
        while threads:
            threads = [t for t in threads if t.is_alive()]
            print(f'\r{len(ids) - len(threads):>3} / {len(ids)}', end='')
        print('\ndone')

        def get_info(index):
            t = songs[index]
            print(f'\n{t}')

            a = input(f'artist = {artists[index]}?\n > ')
            for style in (f'{a}: ', f'{a} - ', f' - {a}', a, f' {a} '):
                t = t.replace(style, '')

            t = (lambda x: x if x else t)(input(f'title = {t}?\n > '))
            print(f'using {t} by {a}')

            return t, a if a else artists[index]

        files = listdir(self.destination)
        for i, url in enumerate(ids):
            src = f'{self.destination}/{url}'
            if src + '.mp3' not in files:
                print(f'{songs[i]} failed to download')
                continue

            title, artist = get_info(i)

            tags = eyed3.load(src)
            tags.tag.images.set(ImageFrame.FRONT_COVER, open(f'./temp/{url}', 'rb').read(), 'image/jpeg')
            tags.tag.artist, tags.tag.title = artist, title
            tags.tag.save(version=eyed3.id3.ID3_V2_3)

            rename(src + '.mp3', f'{self.destination}/{title}.mp3')

            for lang in self.langs:
                f = f'.{lang}.vtt'
                if (url + f) in files:
                    rename(src + f, f'{self.destination}/{title}{f}')
                    move(src + f, f'{self.destination}/subtitles/{title}{f}')
                    break
            else:
                print(f'no subtitles found for {src} with langs {", ".join(self.langs)}')

            for ext in ('.png', '.jpg', 'jpeg', 'webp'):
                if url + ext in files:
                    rename(src + ext, f'{self.destination}/{title}{ext}')
                    move(src + ext, f'{self.destination}/thumbnails/{title}{ext}')
                    break
            else:
                print(f'no image found for {src}')

        if operating_sys == 'posix':
            system(f'open {self.destination}')
        else:
            system(f'start {self.destination}')

        for file in listdir('./temp'):
            remove(f'./temp/{file}')

        print('done')
        exit()

    def run(self):
        self.load_next()
        self.root.mainloop()


def sanitize(s):
    return ''.join(x for x in s if x not in '<>/\\"\':|?*')


if __name__ == '__main__':
    Downloader(2, destination='~/Documents/m').run()
