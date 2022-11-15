from youtube_search import YoutubeSearch as Search
from os import system, listdir, rename, remove
from tkinter import Tk, Canvas, Entry, END, NW
from requests import get
from PIL import Image, ImageTk
from multiprocess import Pool
from yt_dlp.utils import sanitize_filename as yt_sanitize
from shutil import move
import eyed3
from eyed3.id3.frames import ImageFrame


class Downloader:
    def __init__(self, k=None, w=1200, h=800,
                 file='to_download', destination='C:/Users/Administrator/OneDrive/Desktop/folders/music/'):
        self.i = 0
        self.queries = open(file, encoding='UTF-8').read().split('\n')
        if k:
            self.queries = self.queries[:k]

        self.w, self.h = w, h - 100
        self.length = 3
        self.iw, self.ih = self.w * 3 // 10, (self.h - 50) // self.length

        self.data = {}
        self.current = {}
        self.images = {}
        self.image_names = {}
        self.destination = destination

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
            name = f'./temp/{sanitize(video["title"])}.jpg'
            if name[7:] in listdir('./temp'):
                name = name[:-4] + f'{j}.jpg'

            open(name, 'wb').write(get(video['thumbnails'][0]).content)
            self.image_names[sanitize(video['title'])] = name

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

    def back(self, _): self.i -= 1

    def select(self, e):
        if e.y > self.length * self.ih:
            return

        a = self.current[e.y // 250]
        self.data[self.i] = a['id'], a['title'], a['channel']

        self.i += 1
        self.load_next()

    def download_all(self):   # TODO: add id to end of filename, and check if file[-12:-4] is in [ids]
        # TODO: then rewrite all the code to be less shitty & cleanup imports and funcs
        # get yt-dlp on mac & set configs to be the same
        # TODO: config =>
        '''
-x
--audio-format mp3
--write-sub
--sub-langs "en,jp"
--write-thumbnail
-o C:/Users/Administrator/OneDrive/Desktop/folders/music/%(title)s.%(ext)s
--embed-thumbnail
--add-metadata
        '''
        ids, songs, artists = list(zip(*self.data.values()))

        print('\n', '\n'.join(songs), '\n')
        songs = list(map(sanitize, songs))
        print('\n', '\n'.join(songs), '\n')

        Pool(11).map(lambda x: system(f'youtube-dl {x} --rm-cache-dir --no-progress'), ids)

        # threads = list(map(lambda x: Thread(target=lambda: system(f'youtube-dl {x}')), ids))
        # for thread in threads:
        #     thread.start()
        #
        # for i, thread in enumerate(threads):
        #     thread.join()
        #     print(songs[i])

        print('finished downloading')
        for file in listdir(self.destination):
            print(sanitize(file[:-4]))
            src = self.destination + file
            ext = file[-4:]

            if ext == '.mp3' and sanitize(file[:-4]) in songs:
                name = sanitize(file[:-4])

                tags = eyed3.load(f'{self.destination}/{file}')
                tags.tag.images.set(ImageFrame.FRONT_COVER, open(self.image_names[name], 'rb').read(),
                                    'image/jpeg')

                tags.tag.artist = input(f'is {tags.tag.artist} the artist?\n > ')

                t = input('title?\n > ')
                if t:
                    f = f'{self.destination}/{t}.mp3'
                    if f in listdir(self.destination):
                        print(f'\t\toverwriting {f}')
                        remove(f)
                    rename(src, f)
                    tags.tag.title = t

                tags.tag.save(version=eyed3.id3.ID3_V2_3)

                continue

            a, b = ext == '.vtt', ext in ('.jpg', '.png', '.jpeg')

            if not (a or b):
                if ext != '.mp3':
                    print(f'\t\t"{file}" extension ({ext}) was not in (.vtt, .png, .jpeg, .jpg, .mp3)')
                else:
                    print(f'\t\t"{sanitize(file[:-4])}" was not found in songs')
                continue

            folder = self.destination + ('/subtitles/' if a else ('/thumbnails/' if b else ''))

            if file in listdir(folder):
                remove(folder + file)

            move(src, folder)

        system(f'start {self.destination}')
        for file in listdir('./temp'):
            remove(f'./temp/{file}')

        print('done')
        exit()

    def run(self):
        self.load_next()
        self.root.mainloop()


def sanitize(s):
    return yt_sanitize(s.replace("/", "_").replace(' - ', ': ').replace('"', '').replace('”', '').replace('\'', ''))


if __name__ == '__main__':
    Downloader().run()
