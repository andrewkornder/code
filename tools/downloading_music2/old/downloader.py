from youtube_search import YoutubeSearch as Search
from os import system, listdir, remove, path, name as operating_sys
from tkinter import Tk, Canvas, Entry, END, NW, Button
from requests import get
from PIL import Image, ImageTk
from threading import Thread
from youtube_dl import YoutubeDL as Yt
from youtube_dl.utils import DownloadError
from shutil import move
import eyed3
from time import sleep, perf_counter
from eyed3.id3.frames import ImageFrame


class Downloader:
    langs = ['en', 'ja']
    options = {
        'writethumbnail': True,
        'quiet': True,
        'no_warnings': True,
        'retries': 2,
        'cachedir': './cache',
        'nocheckcertificate': operating_sys == 'posix',
        'writesubtitles': True,
        'subtitleslangs': ['en', 'ja'],
        'outtmpl': f'/%(id)s.%(ext)s',
        # 'ffmpeg_location': '/Users/akornder25/Downloads/',
        'postprocessors': [
            {'key': 'FFmpegExtractAudio',
             'preferredcodec': 'mp3'},
            {'key': 'FFmpegMetadata'},
            {'key': 'EmbedThumbnail'},
        ]
    }
    destination = 'C:/Users/Administrator/OneDrive/Desktop/folders/music'

    read = './to_download.txt'
    temp = './temp'
    translator = './translator.txt'
    past = './past_saves.txt'

    def __init__(self, text=None, first_k=None, w=1200, h=800, langs=None,
                 destination=None, translator=None, options=None, auto=False,
                 just_subs=False):
# TODO: make editable list on a sidebar for search queries
        self.i = 0
        self.auto_select = auto
        self.just_subs = just_subs

        self.translate = (lambda *args: args) if translator is None else \
            (translator if translator is not True else self.get_translator(self.translator))

        self.langs = langs.split(',') if langs else self.langs

        self.w, self.h = w, h - 100
        self.length = 3
        self.iw, self.ih = self.w * 3 // 10, (self.h - 50) // self.length

        self.data = {}
        self.current = {}
        self.images = {}

        if destination:
            self.destination = destination.replace('~', path.expanduser('~'))

        if options is not None:
            self.options = options
        else:
            self.options['outtmpl'] = self.destination + self.options['outtmpl']
        self.options['skip_download'] = just_subs

        self.font = ('Niagara Bold', 10)

        self.root = Tk()
        self.root.geometry(f'{self.w}x{h}')

        self.canvas = Canvas(self.root, width=self.w, height=self.h)
        self.canvas.grid(row=0, column=0, columnspan=3)

        self.input = Entry(self.root)
        self.input.grid(row=1, column=1)

        self.toggler = Button(self.root, text='pause?', command=self.toggle_pause)
        self.toggler.grid(row=1, column=2)

        if text is None:
            self.queries = open(self.read, encoding='UTF-8').read().split('\n')
        elif type(text) == list:
            self.queries = text
        else:
            self.queries = open(text.replace('~', path.expanduser('~')), encoding='UTF-8').read().split('\n')

        if first_k:
            self.queries = self.queries[:first_k]

        self.paused = not bool(self.queries)

        self.canvas.bind('<ButtonRelease-1>', lambda e: self.select(e.y // self.ih))
        self.canvas.bind('<ButtonPress-3>', self.back)
        self.root.bind('<Return>', lambda *_: self.enter() if not self.paused else self.get_query())

    def toggle_pause(self, *_):
        self.paused = not self.paused

        if self.paused:
            self.draw_queries()
        else:
            self.load_next()

    def draw_queries(self):
        self.canvas.delete('all')

        x, y = self.w / 2, 0
        for q in self.queries:
            y += 80
            self.canvas.create_text(x, y, text=q, font=self.font)

    def get_query(self, *_):
        if not self.paused:
            return

        self.queries.append(self.input.get())
        self.draw_queries()
        self.input.delete(0, END)

    def load_next(self):
        if self.paused:
            return

        if self.i == len(self.queries):
            self.root.destroy()
            self.finalize()
            return

        self.canvas.delete('all')

        self.current = Search(self.queries[self.i], max_results=self.length).to_dict()
        self.canvas.create_text(self.w / 2, self.ih * self.length + 25, text=self.queries[self.i], font=self.font)

        self.images[self.i] = []
        for j, video in enumerate(self.current):
            name = f'{self.temp}/{video["id"]}.jpg'
            open(name, 'wb').write(get(video['thumbnails'][0]).content)

            im = ImageTk.PhotoImage(Image.open(name).resize((self.iw, self.ih)), master=self.root)
            self.images[self.i].append(im)

            x, y = self.w - self.iw, self.ih * j
            self.canvas.create_image(x, y, anchor=NW, image=self.images[self.i][-1])
            self.canvas.create_text(x / 2, y + self.ih / 2, font=self.font,
                                    text=f"[{video['duration']}] \"{video['title']}\" - {video['channel']}")

        if self.auto_select:
            self.root.after(1, lambda: self.select(0))

    def enter(self, *_):
        self.queries[self.i] = self.input.get()
        self.input.delete(0, END)
        self.load_next()

    def back(self, *_):
        self.i -= 1

    def select(self, i):
        if i >= self.length or self.paused:
            return

        a = self.current[i]
        self.data[self.i] = a['id'], a['title'], a['channel']

        print(a['title'])

        self.i += 1
        self.load_next()

    @staticmethod
    def download(options, x):
        start = perf_counter()
        y = Yt(options)

        def dl2(inputs, k=5):
            def clean(ts):
                ls = []
                for t, u in ts:
                    if t.is_alive():
                        ls.append((t, u))
                    # else:
                    #     print(title_font'colors {u}')

                return ls

            def d(a):
                try:
                    y.download([a])
                except DownloadError:
                    system('youtube-dl --rm-cache-dir --quiet')
                    failed.append(a)

            failed = []
            threads = []
            for n, i in enumerate(inputs):
                threads.append((Thread(target=d, args=(i,)), i))
                threads[-1][0].start()
                print(
                    f'\rstarted {", ".join([z[1] for z in threads])} | finished{n - len(threads) + 2 - len(failed):>3} | failed {len(failed)}',
                    end='')

                while len(threads) == k:
                    threads = clean(threads)
                    sleep(1)

            while threads:
                threads = clean(threads)
                sleep(1)

            return failed

        def dl(inputs):
            failed = []
            for i in inputs:
                try:
                    y.download([i])
                    print(f'[{(perf_counter() - start) / 60:.1f}] downloaded {i}')
                except DownloadError:
                    failed.append(i)
                    print(f'failed to download {i}')

            return failed

        retry = dl2(x)
        while retry:
            print(f'\n{len(retry)} downloads failed: restarting')
            second = dl(retry)
            if len(retry) == len(second):
                return second
            retry = second

    def finalize(self):
        ids, songs_o, artists = list(zip(*self.data.values()))
        songs = list(map(self.sanitize, songs_o))

        past = set(open(self.past, encoding='utf-8').read().split('\n'))
        trans = set(open(self.translator, encoding='utf-8').read().split('\n'))

        system('youtube-dl --rm-cache-dir')
        self.download(self.options, ids)

        print('finished downloading')
        print(ids)

        def get_info(index):
            def func(a, b): return a if a else b

            (current_title, current_artist) = self.translate(songs[index], artists[index])
            print(f'\n{current_title}')

            current_artist = func(input(f'artist = {current_artist}?\n > '), current_artist)
            for style in (f'{current_artist}: ', f'{current_artist} - ', f' - {current_artist}',
                          current_artist, f' {current_artist} ', f' - {current_artist} MV'):
                current_title = current_title.replace(style, '')

            current_title = func(input(f'title = {current_title}?\n > '), current_title)
            print(f'using {current_title} by {current_artist}')

            return current_title, current_artist

        files = [x for x in listdir(self.destination) if path.isfile(self.destination + '/' + x)]

        print('\n'.join(f'{a:<20}{b}' for a, b in zip(*(lambda l: (files[:l // 2], files[l // 2:]))(len(files)))), '\n')

        for i, url in enumerate(ids):
            src = f'{self.destination}/{url}'
            if url + '.mp3' not in files:
                print(f'{songs[i]} failed to download')
                continue

            title, artist = get_info(i)

            past.add(f'{url}|{songs_o[i]}')
            trans.add(f'{songs_o[i]} : {title} | {artist}')

            tags = eyed3.load(src + '.mp3')
            tags.tag.images.set(ImageFrame.FRONT_COVER, open(f'{self.temp}/{url}.jpg', 'rb').read(), 'image/jpeg')
            tags.tag.artist, tags.tag.title = artist, title
            tags.tag.save(version=eyed3.id3.ID3_V2_3)

            move(src + '.mp3', f'{self.destination}/mp3s/{title}.mp3')
            for lang in self.langs:
                extension = f'.{lang}.vtt'
                if (url + extension) in files:
                    move(src + extension, f'{self.destination}/subtitles/{title}{extension}')
                else:
                    print(f'no subtitles found for "{title}" with langs {lang}')

            move(f'{self.temp}/{url}.jpg', f'{self.destination}/thumbnails/{title}.jpg')

        system(f'{"open" if operating_sys == "posix" else "start"} {self.destination}')

        for temp in listdir(self.temp):
            remove(f'{self.temp}/{temp}')

        open(self.past, 'w', encoding='utf-8').write('\n'.join(past))
        open(self.translator, 'w', encoding='utf-8').write('\n'.join(trans))

    def run(self):
        if not self.paused:
            self.load_next()

        self.root.mainloop()
        return self.data

    @staticmethod
    def sanitize(s):
        return ''.join(x for x in s if x not in '<>/\\"\':|?*')

    @classmethod
    def restore(cls, options=None):
        cls.download(options if options else cls.options, [a[:10] for a in open(cls.past).read().split('\n')])

    @staticmethod
    def get_translator(file):
        t0, t1, t2 = zip(*[(lambda x: (x[0].strip(), *(lambda x: x if len(x) == 2 else ['', ''])(x[1].split(' | ')))) \
                               (a.split(' : ')) for a in open(file, encoding='utf-8').read().split('\n')])
        t = dict(zip(t0, zip(t1, t2)))
        return lambda x, n: (x, n) if x not in t else (lambda y, a: y if y[1] else (y[0], a))(t[x], n)


if __name__ == '__main__':
    folder = '~/Documents/GitHub/folders/music/' if operating_sys == 'posix' else \
        '~/OneDrive/Desktop/folders/music'

    _ids = Downloader(destination=folder, translator=True, auto=1).run()
