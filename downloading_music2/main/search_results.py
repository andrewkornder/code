from threading import Thread
from PIL import ImageTk, Image
from requests import get
from youtubesearchpython import VideosSearch
from tkinter import Frame, Canvas
from editable_list import EditableList
from functools import cache


class SearchResults:
    background = '#333333'

    def __init__(self, root, w, h, length, grid, title_font, searches, tree, past, temp, auto=False):
        # we dont really care about the title, since the url uniquely identifies the video
        self.past = [a.split(' | ') for a in open(past, encoding='utf-8').read().split('\n') if a]
        self.past_ids = list(map(lambda x: x[1], self.past))

        self.temp = temp

        lwidth = min(title_font.measure(max(searches, key=len)), w // 6)
        self.w, self.h = w - lwidth, h
        self.length = length

        self.ih = self.h // self.length
        self.iw = int(16 / 9 * self.ih)
        self.border = self.w - self.iw

        self.font = title_font

        self.results, self.results, self.searches = {i: None for i in range(len(searches))}, {}, searches
        self.load_searches()

        self.images = []
        self.chosen = {}
        self.i = 0
        self.auto = auto
        self.ended = False

        self.root = root
        self.frame = Frame(self.root)
        self.frame.grid(**grid)

        self.canvas = Canvas(self.frame, width=self.w, height=h, bg=self.background)
        self.canvas.pack(side='left')

        self.canvas.bind('<ButtonRelease-1>', lambda e: self.select(e.y // self.ih))

        self.root.bind('<Left>', self.back)
        self.root.bind('<BackSpace>', self.remove)
        self.root.bind('<Right>', self.skip)
        self.root.bind('<Tab>', self.toggle_auto)

        self.tree = tree
        self.queries_t = EditableList(self.frame, lwidth, h, len(searches), ('query',),
                                      {'side': 'right'}, entries=list(zip(self.searches)),
                                      tags=[('all', a) for a in self.searches])

        def on_edit(entries, args):
            i = self.searches.index(args[0])
            self.searches[i] = entries[0].get()
            self.results[i] = None
            Thread(target=self.get_search, args=(i, self.searches[i])).start()

            if self.i == i:
                self.search()

        self.queries_t.on_edit = on_edit

    def remove(self, *_):
        self.tree.add(self.i, ('', ''), '')

    def toggle_auto(self, *_):
        self.auto = not self.auto
        self.select(0)

    def back(self, *_):
        if (self.i - 1) not in self.results:
            return
        self.i -= 1
        self.search()

    def skip(self, *_):
        if (self.i + 1) not in self.results:
            return
        self.i += 1
        self.search()

    def get_search(self, index, q):  # TODO: add second page and button for turning page
        @cache
        def levenshtein(s1, s2):
            if len(s1) < len(s2):
                return levenshtein(s2, s1)

            if len(s2) == 0:
                return len(s1)

            previous_row = range(len(s2) + 1)
            for i, c1 in enumerate(s1):
                current_row = [i + 1]
                for j, c2 in enumerate(s2):
                    insertions = previous_row[j + 1] + 1
                    deletions = current_row[j] + 1
                    substitutions = previous_row[j] + (c1 != c2)
                    current_row.append(min(insertions, deletions, substitutions))
                previous_row = current_row

            return previous_row[-1]

        def score(video):
            if video['id'] not in self.past_ids:
                return levenshtein(q, video['title'])

            title = self.past[self.past_ids.index(video['id'])][0]
            return levenshtein(title, video['title'])

        def scrape(video):
            new = {
                'artist': video['channel']['name'],
                'title': video['title'],
                'duration': video['duration'],
                'thumbnails': video['thumbnails'],
                'id': video['id']
            }
            return new

        result = list(map(scrape, VideosSearch(q, limit=self.length).result()['result']))
        self.results[index] = sorted(result, key=score)

    def load_searches(self):
        for i, query in enumerate(self.searches):
            Thread(target=self.get_search, args=(i, query)).start()

    def add(self, query):
        self.tree.table.insert('', 'end', values=('', ''), iid=str(len(self.searches)))
        self.queries_t.add(len(self.searches), query)
        self.searches += (query,)
        Thread(target=self.get_search, args=(len(self.searches) - 1, query)).start()

        if self.ended:
            self.ended = False
            self.search()

    def draw(self, video):
        name, text = f'{self.temp}/{video["id"]}.jpg', f"[{video['duration']}] \"{video['title']}\""
        open(name, 'wb').write(get(max(video['thumbnails'], key=lambda x: x['width'])['url']).content)

        y = self.ih * len(self.images)

        im = ImageTk.PhotoImage(Image.open(name).resize((self.iw, self.ih)), master=self.canvas)
        self.images.append(im)

        border_w = 8
        if video['id'] in self.past_ids:
            self.canvas.create_rectangle(0, y, self.border, y + self.ih, fill='#ff3333', tags=('bg',))
        self.canvas.create_rectangle(border_w, y + border_w, self.border - border_w, y - border_w + self.ih,
                                     outline='', fill=self.background, tags=('bg',))
        self.canvas.tag_lower('bg')

        self.canvas.create_image(self.border, y, anchor='nw', image=self.images[-1])
        self.canvas.create_text(self.border / 2, y + self.ih / 2, font=self.font,
                                text=f"{text}\n{video['artist']:^{len(text)}}")

    def select(self, i):
        if self.i not in self.results or i >= len(self.results[self.i]):
            return

        selection = self.results[self.i][i]
        u, info = selection['id'], (selection['title'], selection['artist'])

        self.results[u] = info
        self.chosen[self.i] = i
        self.tree.add(self.i, (*info, u), u)

        self.i += 1
        self.search()

    def draw_load(self):
        self.canvas.delete('all')
        self.canvas.create_text(400, 400, text='loading')
        # TODO: loading page

    def search(self):
        if self.i == len(self.searches):
            self.ended = True
            self.auto = False
            return

        self.draw_load()
        if self.i not in self.results or self.results[self.i] is None:
            self.root.after(500, self.search)
            return

        self.queries_t.table.tag_configure('all', background='white')
        self.queries_t.table.tag_configure(self.searches[self.i], background='green')
        self.canvas.delete('all')
        self.images = []
        for v in self.results[self.i]:
            self.draw(v)

        if self.auto:
            self.root.after(1, lambda: self.select(0))
