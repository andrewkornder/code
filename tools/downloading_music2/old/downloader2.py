from youtube_search import YoutubeSearch as Search
from os import system, listdir, remove, path, name as operating_sys
from tkinter import Tk, Canvas, Entry, Button, Scrollbar, Listbox, Toplevel, Label
from tkinter.font import Font
from requests import get
from PIL import Image, ImageTk
from threading import Thread
from youtube_dl import YoutubeDL as Yt
from youtube_dl.utils import DownloadError
from shutil import move
import eyed3
from time import sleep, perf_counter
from eyed3.id3.frames import ImageFrame


TEMP, PAST, TRANSLATOR = './temp', './past_saves.txt', './translator.txt'


class SearchResults:
    def __init__(self, root, titles, artists, w, h, row, col):
        self.length = 3
        self.w, self.h = w, h

        self.ih = h // self.length
        self.iw = self.ih * 16 // 9
        self.border = self.w - self.iw

        self.canvas = Canvas(root, width=w, height=h, bg='#222222')
        self.canvas.grid(row=row, column=col)

        self.images = []
        self.queue = Queue(self)
        self.titles, self.artists = titles, artists
        self.ids = []

        self.current = []
        self.paused = True

        self.canvas.bind('<ButtonRelease-1>', lambda e: self.select(e.y // self.ih))
        self.canvas.bind('<space>', lambda e: self.queue.skip)

    def draw_result(self, video):
        name = f'{TEMP}/{video["id"]}.jpg'
        open(name, 'wb').write(get(video['thumbnails'][0]).content)

        im = ImageTk.PhotoImage(Image.open(name).resize((self.iw, self.ih)), master=self.canvas)
        self.images.append(im)

        y = self.ih * (len(self.images) - 1)
        self.canvas.create_image(self.border, y, anchor='nw', image=self.images[-1])
        self.canvas.create_text(self.border / 2, y + self.ih / 2, font=FONT,
                                text=f"[{video['duration']}] \"{video['title']}\" - {video['channel']}")

    def select(self, i):
        if i >= len(self.current):
            return

        video = self.current[i]
        self.titles.add(video['title'])
        self.artists.add(video['channel'])
        self.ids.append(video['id'])

        self.current = []

    def search(self, query):
        if not query:
            self.paused = False
            return

        self.paused = True
        self.canvas.delete('all')

        self.current = Search(query, max_results=self.length).to_dict()

        for video in self.current:
            self.draw_result(video)

        self.search(self.queue.next)


class EditableList:
    def __init__(self, root, row, col, height, formatter=lambda *args: args):
        self.root = root

        self.list_box = Listbox(root, width=30, height=height, selectmode="multiple")
        self.list_box.grid(row=row, column=col)

        self.scrollbar = Scrollbar(self.list_box)
        self.scrollbar.pack(side='right', fill='both')

        self.list_box.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.list_box.yview)

        self.items = []
        self.formatter = formatter

        self.list_box.bind('<<ListboxSelect>>', self.edit)

    def edit(self, event):
        selection = event.widget.curselection()
        if not selection:
            return

        print(selection)  # TODO

    def pop_up(self, text):
        def finish(*_):
            self.items.remove(text)
            i = self.list_box.get(0, 'end').index(text)
            self.list_box.delete(i)

            self.list_box.insert(i, entry.get())
            self.items.append(entry.get())

            top.destroy()

        top = Toplevel(self.root)
        top.geometry("500x300")
        top.title('Editing Window')

        Label(top, text=f'edit {text} to:', font=FONT).grid(row=0, column=0)
        entry = Entry(top, font=FONT)
        entry.grid(row=1, column=0)

        top.bind('<Return>', finish)

    def add(self, item):
        self.items.append(item)
        self.list_box.insert('end', self.formatter(item))


class SearchBar:
    def __init__(self, root, search, queue, row, col):
        self.root = root
        self.search = search

        self.entry = Entry(root, width=30)
        self.entry.grid(row=row, column=col)

        self.queue = queue
        self.entry.bind('<Return>', lambda *_: (self.queue.add(self.entry.get()), self.entry.delete(0, 'end')))


class Downloader:
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
        'postprocessors': [
            {'key': 'FFmpegExtractAudio',
             'preferredcodec': 'mp3'},
            {'key': 'FFmpegMetadata'},
            {'key': 'EmbedThumbnail'},
        ]
    }

    def __init__(self, overrides, dest, threads=False):
        self.options['outtmpl'] = dest + self.options['outtmpl']
        for k, v in overrides.items():
            self.options[k] = v

        self.running = None

        #self.download = self.with_threads if threads else self.threadless

        self.youtube = Yt(self.options)

    def threadless(self, links):
        def dl(urls):
            failed = []
            for i, link in enumerate(urls):
                try:
                    self.youtube.download([link])
                    print(f'[{i:>2}] finished {link}')
                except DownloadError:
                    print(f'\t\t\tfailed to download {link}')
                    failed.append(link)
            return failed

        returned = dl(links)
        while returned:
            print(f'{len(returned)} videos failed to download')
            tmp = dl(returned)
            if len(tmp) == len(returned):
                print(f'giving up on videos {", ".join(returned)}')
                return tmp
            returned = tmp

        return []

    def with_threads(self, links):
        def clean(iterable):
            return [t for t in iterable if t.is_alive()]

        def dl(i, link):
            try:
                self.youtube.download([link])
                print(f'[{i:>2}] finished {link}')
            except DownloadError:
                print(f'\t\t\tfailed to download {link}')
                failed.append(link)

        threads, k = [], 10
        failed = []
        for i, url in enumerate(links):
            thread = Thread(target=dl, args=(i, url))
            threads.append(thread)
            thread.start()

            while len(threads) == k:
                threads = clean(threads)
                sleep(1)

        while threads:
            threads = clean(threads)
            sleep(1)

        return failed


class Queue:
    def __init__(self, parent):
        self.queries = []
        self.parent = parent

    def add(self, item):
        print('\n'.join(self.queries) + '\n' + item)
        self.queries.append(item)
        if self.parent.paused:
            self.parent.search(self.next)

    def skip(self):
        self.next()

    @property
    def next(self):
        if not self.queries:
            return None

        x = self.queries[0]
        del self.queries[0]
        return x


class Display:
    def __init__(self, file, folder, w, h, **kwargs):
        q = Downloader(kwargs, folder)
        self.root, self.titles, self.artists, self.search, self.input_box = self.window(w, h)
        self.root.mainloop()

    def window(self, w, h):
        root = Tk()
        root.geometry(f'{w}x{h}')

        global FONT
        FONT = Font(root, size=10, family='Niagara Bold')

        # TOP ROW OF WINDOW

        titles = EditableList(root, row=0, col=0, height=20)
        artists = EditableList(root, row=0, col=2, height=20)

        sw, sh = w - 200, h - 100
        search = SearchResults(root, titles, artists, row=0, col=1, w=sw, h=sh)

        # BOTTOM ROW OF WINDOW

        input_box = SearchBar(root, search, search.queue, row=1, col=1)

        return root, titles, artists, search, input_box


if __name__ == '__main__':
    Display('', 'C:/Users/Administrator/OneDrive/Desktop/folders/music', 1600, 800)