from youtube_search import YoutubeSearch as Search
from os import system, listdir, rename, remove, path, name as operating_sys
from tkinter import Tk, Canvas, Entry, END, NW
from requests import get
from PIL import Image, ImageTk
from threading import Thread
from youtube_dl import YoutubeDL as yt
from shutil import move
import eyed3
from eyed3.id3.frames import ImageFrame


class Downloader:
    def __init__(self, text,k=None, w=1200, h=800, langs='en,ja',
                 destination='C:/Users/Administrator/OneDrive/Desktop/folders/music',
                 translator=None):
        self.i = 0

        self.queries = (text if '\n' in text else open(text, encoding='UTF-8').read()).split('\n')
        self.translate = (lambda *args: args) if translator is None else translator

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

        self.canvas.bind('<ButtonRelease-1>', lambda e: self.select(e.y // self.ih))
        self.canvas.bind('<ButtonPress-3>', self.back)
        self.root.bind('<Return>', self.enter)

    def load_next(self):
        if self.i == len(self.queries):
            self.root.destroy()
            self.finalize()
            return

        self.canvas.delete('all')

        self.current = Search(self.queries[self.i], max_results=self.length).to_dict()

        self.canvas.create_text(self.w / 2, self.ih * self.length + 25, text=self.queries[self.i], font=self.font)

        self.images[self.i] = []
        for j, video in enumerate(self.current):
            name = f'../temp/{video["id"]}.jpg'

            open(name, 'wb').write(get(video['thumbnails'][0]).content)

            im = ImageTk.PhotoImage(Image.open(name).resize((self.iw, self.ih)), master=self.root)
            self.images[self.i].append(im)

            ic = self.w - self.iw, self.ih * j
            self.canvas.create_image(*ic, anchor=NW, image=self.images[self.i][-1])
            self.canvas.create_text(ic[0] / 2, (j + 0.5) * self.ih, font=self.font,
                                    text=f"[{video['duration']}] \"{video['title']}\" - {video['channel']}")

        # self.select(0)

    def enter(self, _):
        self.queries[self.i] = self.input.get()
        self.input.delete(0, END)
        self.load_next()

    def back(self, _):
        self.i -= 1

    def select(self, i):
        if i >= self.length:
            return

        a = self.current[i]
        self.data[self.i] = a['id'], a['title'], a['channel']

        print(a['title'])

        self.i += 1
        self.load_next()

    def finalize(self):
        ids, songs, artists = list(zip(*self.data.values()))

        songs = list(map(self.sanitize, songs))

        system('youtube-dl --rm-cache-dir --quiet')
        yt({
            'writethumbnail': True,
            'quiet': True,
            'writesubtitles': True,
            'subtitleslangs': self.langs,
            'outtmpl': f'{self.destination}/%(id)s.%(ext)s',
            'postprocessors': [
                {'key': 'FFmpegExtractAudio',
                 'preferredcodec': 'mp3'},
                {'key': 'FFmpegMetadata'},
                {'key': 'EmbedThumbnail'},
            ]
        }).download(ids)

        print('finished downloading')

        def get_info(index):
            (t, a), func = self.translate(songs[index], artists[index]), lambda x, b: x if x else b
            print(f'\n{t}')

            a = func(input(f'artist = {artists[index]}?\n > '), a)
            for style in (f'{a}: ', f'{a} - ', f' - {a}', a, f' {a} '):
                t = t.replace(style, '')

            t = func(input(f'title = {t}?\n > '), t)
            print(f'using {t} by {a}')

            return t, a

        files = [x for x in listdir(self.destination) if path.isfile(self.destination + '/' + x)]

        print('\n'.join(f'{a:<20}{b}' for a, b in zip((lambda l: (files[:l // 2], files[l//2:]))(len(files)))), '', sep='\n')

        for i, url in enumerate(ids):
            src = f'{self.destination}/{url}'
            if url + '.mp3' not in files:
                print(f'{songs[i]} failed to download')
                continue

            title, artist = get_info(i)

            tags = eyed3.load(src + '.mp3')
            tags.tag.images.set(ImageFrame.FRONT_COVER, open(f'../temp/{url}.jpg', 'rb').read(), 'image/jpeg')
            tags.tag.artist, tags.tag.title = artist, title
            tags.tag.save(version=eyed3.id3.ID3_V2_3)

            rename(src + '.mp3', f'{self.destination}/{title}.mp3')
            for lang in self.langs:
                f = f'.{lang}.vtt'
                if (url + f) in files:
                    move(src + f, f'{self.destination}/subtitles/{title}{f}')
                else:
                    print(f'no subtitles found for "{title}" with langs {lang}')

            move(f'../temp/{url}.jpg', f'{self.destination}/thumbnails/{title}.jpg')

        system(f'{"open" if operating_sys == "posix" else "start"} {self.destination}')

        for file in listdir('./temp'):
            remove(f'../temp/{file}')

        exit()

    def run(self):
        self.load_next()
        self.root.mainloop()

    @staticmethod
    def sanitize(s):
        return ''.join(x for x in s if x not in '<>/\\"\':|?*')


if __name__ == '__main__':
    t = dict(zip('Mao Abe／阿部真央 - まだいけます|幼女戦記 ED  Youjo Senki Ending 「FULL」 - Los! Los! Los! -  Tanya Degurechaff (悠木 碧)|【Ado】”罪と罰  Crime & Punishment 歌いました|Persona 4 Dancing All Night Opening Theme|砂の惑星  ハチ(cover) - Eve|太陽系デスコ  ナユタン星人(cover) - Eve|Flamingo Instrumental|Seishun Buta Yarou wa Bunny Girl Senpai no Yume wo Minai ED [Part Section]「Fukashigi no Carte」|Jake Chudnow - Moon Men (Instrumental)|jump man 93 - bruh|[KanjiRomajiEnglish] Hyouka-Madoromi no Yakusoku (Ending 1) まどろみの約束|[Hyouka] OP 2, Full Version - Mikansei Stride|Pax - Gee (Disco Remix)|PSYQUI - Fly to the moon feat. 中村さんそ|PSYQUI - Start Up feat. Such|PSYQUI - ヒステリックナイトガール feat. Such (android52 Edit)|android 52 - romance|android52 - super anime groove 3d world|Super Mario World Game Over LoFi Hip Hop Remix|Nanidato (ナニダト) - SUPER RISER! (Remake)|惑星ループ - Eve  feat.ナユタン星人'.split('|'), zip('まだいけます|Los! Los! Los!|罪と罰|Dancing All Night|砂の惑星|太陽系デスコ|Flamingo|Fukashigi no Carte|Moon Men|bruh|まどろみの約束|Mikansei Stride|Gee|Fly to the moon feat. 中村さんそ|Start Up feat. Such|ヒステリックナイトガール feat. Such (android52 edit)|romance|super anime groove 3d world|Super Mario World Game Over|SUPER RISER!|惑星ループ feat. ナユタン星人|'.split('|'), '阿部真央||Ado||Eve|Eve|||Jake Chudnow|jump man 93|||Pax|PSYQUI|PSYQUI|PSYQUI|android52|android52||ナニダト|Eve'.split('|'))))
    f = lambda x, n: (x, n) if x not in t else (lambda y, a: y if y[1] else (y[0], a))(t[x], n)
    Downloader(r'E:\code\downloading_music2\to_download', translator=f).run()
