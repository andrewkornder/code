from threading import Thread
from PIL import ImageTk, Image
from numpy import pi, cos, sin
from requests import get
from youtubesearchpython import VideosSearch
from tkinter import Frame, Canvas, Label, Button
from editable_list import EditableList
from functools import cache
from search_bar import SearchBar


class SearchResults:
    background = '#333333'

    def __init__(self, root, w, h, length, grid, title_font, searches, tree, past, temp, pages=3, auto=False,
                 strict_prev=False):
        self.past_titles, self.past_ids = zip(*[a.split(' | ') for a in open(past, encoding='utf-8').read().split('\n')
                                                if a])

        self.temp = temp

        max_len_q = max(searches, key=len)
        line_width = min(title_font.measure(max_len_q), w // 6)
        self.w, self.h = w - line_width, h - 60
        self.length = length

        self.ih = self.h // self.length
        self.iw = int(16 / 9 * self.ih)
        self.border = self.w - self.iw

        self.font = title_font

        self.pages, self.page = pages, 0
        self.results, self.searches = {i: None for i in range(len(searches))}, searches
        self.load_searches()

        self.images = []
        self.chosen = {}
        self.i = 0
        self.auto, self.strict_prev = auto, strict_prev
        self.ended = False

        self.root = root
        self.total_frame = Frame(self.root)
        self.minor_frame = Frame(self.total_frame)

        self.total_frame.grid(**grid)
        self.minor_frame.grid(row=0, column=0, columnspan=5)

        self.canvas = Canvas(self.minor_frame, width=self.w, height=self.h, bg=self.background)
        self.canvas.pack(side='left')

        self.canvas.bind('<ButtonRelease-1>', lambda e: self.select(e.y // self.ih))

        self.root.bind('<Left>', self.back)
        self.root.bind('<BackSpace>', self.remove)
        self.root.bind('<Right>', self.skip)
        self.root.bind('<Tab>', self.toggle_auto)

        self.tree = tree
        self.queries_t = EditableList(self.minor_frame, line_width, self.h, len(searches), ('query',),
                                      {'side': 'right'}, entries=list(zip(self.searches)),
                                      tags=[('all', str(i)) for i in range(len(self.searches))])
        self.queries_t.table.bind('<Button-1>', self.jump_to)

        def on_edit(entries, args):
            i = self.searches.index(args[0])
            self.searches[i] = entries[0].get()
            self.results[i] = None
            Thread(target=self.get_search, args=(i, self.searches[i])).start()

            if self.i == i:
                self.search()

        self.queries_t.on_edit = on_edit

        # [ [<] [page_n] [>]    [search_bar]    [query] ]
        self.page_arrows = [Button(self.total_frame, text='< >'[1 + inc], font=title_font,
                                   command=lambda inc=inc: self.change_page(inc)) for inc in (-1, 1)]
        [button.grid(row=1, column=2 * i) for i, button in enumerate(self.page_arrows)]
        self.page_arrows[0]['state'] = 'disabled'

        self.page_n = Label(self.total_frame, font=title_font, text='Loading')
        self.page_n.grid(row=1, column=1)

        SearchBar(self.root, self, {'row': 1, 'column': 3}, font=title_font)

        self.query_dis = Label(self.total_frame, font=title_font,
                               width=len(max_len_q), text=self.searches[0])
        self.query_dis.grid(row=1, column=4)

    def change_page(self, add):
        self.page += add
        if not self.page:
            self.page_arrows[0]['state'] = 'disabled'
        else:
            self.page_arrows[0]['state'] = 'normal'

        if self.page == self.pages - 1:
            self.page_arrows[1]['state'] = 'disabled'
        else:
            self.page_arrows[1]['state'] = 'normal'

        self.search()

    def jump_to(self, e):
        self.reset_page()
        self.queries_t.highlight(self.i, color='white')
        self.i = int(self.queries_t.table.identify_row(e.y))

        self.search()

    def remove(self, *_):
        self.tree.add(self.i, ('', ''), '')

    def toggle_auto(self, *_):
        self.auto = not self.auto
        self.select(0)

    def reset_page(self):
        self.page = 0

        self.page_n['text'] = f'page 0 of {self.pages}'
        self.page_arrows[0]['state'] = 'disabled'
        self.page_arrows[1]['state'] = 'normal'

    def back(self, *_):
        if (self.i - 1) < 0:
            return
        self.queries_t.highlight(self.i, color='white')
        self.i -= 1
        self.reset_page()
        self.search()

    def skip(self, *_):
        if (self.i + 1) >= len(self.searches):
            return

        self.queries_t.highlight(self.i, color='white')
        self.i += 1
        self.reset_page()
        self.search()

    def get_search(self, index, q):
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
                return levenshtein(q, video['title']) + 10

            title = self.past_titles[self.past_ids.index(video['id'])][0]
            return 0.5 * levenshtein(title, video['title'])

        def scrape(video):
            _n = {
                'artist': video['channel']['name'],
                'title': video['title'],
                'duration': video['duration'],
                'thumbnails': video['thumbnails'],
                'id': video['id']
            }
            return _n

        result = list(map(scrape, VideosSearch(q, limit=self.pages * self.length).result()['result']))
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

        self.chosen[self.i] = i
        self.tree.add(self.i, (*info, u), u)

        self.queries_t.highlight(self.i, color='white')
        self.i += 1
        self.reset_page()
        self.search()

    def draw_load(self, frame):
        self.canvas.delete('all')
        circles, fade_out, s = 10, 3, self.w / 128
        cx, cy, k = self.w / 2, self.h / 2, 2 * pi / circles
        for i in range(1, fade_out + 1):
            angle = k * (i + frame)
            x, y, c = cx + 4 * cos(angle) * s, cy + 4 * sin(angle) * s, i * 255 // fade_out
            self.canvas.create_oval(x - s, y - s, x + s, y + s,
                                    fill='#' + f'{max(0, c - i):02x}{c:02x}{c:02x}', outline='')

    def search(self, frame=0):
        if self.i == len(self.searches):
            self.ended = True
            self.auto = False
            return

        if self.i not in self.results or self.results[self.i] is None:
            self.draw_load(frame)
            self.root.after(125, lambda: self.search(frame + 1))
            return

        self.canvas.delete('all')
        self.images = []

        self.page_n['text'] = f'page {self.page + 1} of {self.pages}'
        self.query_dis['text'] = self.searches[self.i]

        self.queries_t.highlight(self.i)

        for v in self.results[self.i][self.page * self.length:(self.page + 1) * self.length]:
            self.draw(v)

        if self.auto:
            if self.strict_prev and self.results[0]['id'] not in self.past_ids:
                return
            self.root.after(1, lambda: self.select(0))
