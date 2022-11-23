#!/usr/bin/python
# editable_list.py
__author__ = "Andrew Kornder"
__version__ = '1.0'


from os import remove, listdir
from shutil import move
from subprocess import run
from PIL import Image
from eyed3 import id3, load
from eyed3.id3.frames import ImageFrame
from multiprocess import Process
from tkinter import Toplevel, Label, Entry, Button, Frame
from tkinter.font import Font
from tkinter.ttk import Style, Treeview
from pytube import YouTube


class EditableList:
    restricted_letters = ''

    def __init__(self, root, w, h, rows, columns, pack, entries=(), tags=(), font=None):
        self.root = root
        self.columns, self.h = columns, h

        row_height = min(max(15, h // (rows + 2)), 50)
        self.rows = min(rows, h // 15 - 2)
        self.bottom, self.top = self.rows - 1, 0
        font = font if font else Font(font='TkDefaultFont')
        self.style = Style(self.root)

        self.style.configure('Treeview', rowheight=row_height, font=font)
        self.style.configure("Treeview.Heading", font=font)

        self.table = Treeview(self.root, columns=columns, selectmode='extended',
                              show='headings', height=self.rows)
        self.table.pack(**pack)

        self.table.bind("<Button-3>", self.edit)
        self.table.bind("<MouseWheel>", self.on_scroll)
        self.id_table, self.ignore = {}, []

        for heading, width in zip(columns, w if type(w) in (list, tuple) else [w] * len(columns)):
            self.table.heading(heading, text=heading.upper())
            self.table.column(heading, anchor='center', stretch=True, width=width)
        for i, (v, t) in enumerate(zip(entries, tags)):
            self.add(i, v, t if isinstance(t, tuple) else (t,))

    def edit(self, e):
        iid, selection = str(self.table.identify('row', e.x, e.y)), self.table.selection()
        if iid not in self.ignore and iid not in selection:
            self.pop_up(iid, *self.table.item(iid)['values'])

        for iid in selection:
            if iid in self.ignore:
                continue
            self.pop_up(iid, *self.table.item(iid)['values'])

    def on_edit(self, *_):
        return

    def pop_up(self, iid, *args):
        def r(*_): [(lambda e, x: [e.delete(0, 'end'), e.insert(0, x)])(*y) for y in zip(entries, args)]
        def m(x): return min(max(15, 5 * len(x) // 4), 35)
        def v(x, t): return (x not in self.restricted_letters) if t else True

        def finish(*_):
            self.on_edit(entries, args)

            self.table.delete(iid)
            tag = self.id_table[iid] if iid in self.id_table else ''
            self.table.insert('', int(iid), iid=iid, values=tuple(e.get() for e in entries), tags=(tag,))

            top.destroy()

        top = Toplevel(self.root)
        top.title('Editing Window')

        lc = len(self.columns)
        for i, c in enumerate(self.columns):
            Label(top, text=c).grid(row=0, column=2 * i + (lc == 1))

        entries = [Entry(top, width=m(arg), validate="key",
                         validatecommand=(top.register(v), '%S', '%d')) for arg in args]
        [entry.grid(row=1, column=2 * i + (lc == 1)) for i, entry in enumerate(entries)]

        b = None
        for te, col, func in zip('reset enter? cancel'.split(), (0, lc - (lc != 1), 2 * (lc + (lc == 1)) - 2),
                                 (r, finish, lambda *_: top.destroy())):
            b = Button(top, text=te, width=10, command=func)
            b.grid(row=2, column=col)

        r()
        top.update_idletasks()
        top.geometry(f'{b.winfo_width() * ((lc == 1) + 1) + sum(e.winfo_width() for e in entries)}x{75}')

        top.bind('<Return>', finish)
        top.bind('<Escape>', lambda *_: top.destroy())
        top.mainloop()

    def on_scroll(self, e):
        u = int(-1 * (e.delta / 120))
        self.table.yview_scroll(u, 'units')
        self.bottom += u
        self.top += u

    def highlight(self, row, color='green'):  # TODO: look into methods for row visible or not
        if row > self.bottom:
            self.table.yview_scroll(row - self.bottom, 'units')
            self.bottom = row
        elif row <= self.top:
            self.table.yview_scroll(row - self.top - 1, 'units')
            self.top = row

        self.table.tag_configure(str(row), background=color)

    def add(self, index, values, tags=()):
        iid = str(index)
        if self.table.exists(iid):
            self.table.delete(iid)
        self.table.insert('', index, iid=iid, values=values, tags=(tags,) if type(tags) == str else tags)
        self.id_table[iid] = tags


class DownloadList(EditableList):
    @staticmethod
    def download_video(info, params):
        title, artist, url = info
        dest, temp, langs, skip, no_overwrite = params

        if no_overwrite and title + '.mp3' in listdir(f'{dest}/mp3s'):
            return

        fsi = f'{dest}/thumbnails/original/{title}.jpg'
        sqi = f'{dest}/thumbnails/square/{title}.jpg'

        move(f'{temp}/{url}.jpg', fsi)

        sq = Image.open(fsi)
        sq.resize((sq.size[0], sq.size[0]), box=(sq.size[0] / 2 - sq.size[1] / 2, 0,
                                                 sq.size[0] / 2 + sq.size[1] / 2, sq.size[1])
                  ).save(sqi)

        video = YouTube(f'https://www.youtube.com/embed/{url}')

        for lang in langs:
            if lang in video.captions:
                open(f'{dest}/subtitles/{lang}/{title}.txt', 'w', encoding='utf-8').write(
                    '\n'.join(t_i for i, t_i in enumerate(video.captions[lang].generate_srt_captions().split('\n'))
                              if i % 4 == 2)
                )

        if skip:
            return

        mp4, mp3 = f'{dest}/{title}.mp4', f'{dest}/mp3s/{title}.mp3'
        video.streams.filter(type='audio').first().download(dest, filename=mp4)

        run([
            'ffmpeg',
            '-i', mp4, mp3
        ], capture_output=True)
        remove(mp4)

        tags = load(mp3)
        tags.tag.images.set(ImageFrame.FRONT_COVER,
                            open(sqi, 'rb').read(), 'image/jpeg')
        tags.tag.artist, tags.tag.title, tags.tag.album = artist, title, title
        tags.tag.images.set(type_=18, img_data=None, mime_type=None, description=video.description,
                            img_url=video.thumbnail_url)
        tags.tag.save(version=id3.ID3_V2_3)

    @staticmethod
    def get_translator(file):
        t = dict((lambda x: (x[0], x[1].split(' | ')))(a.split(' : '))
                 for a in open(file, encoding='utf-8').read().split('\n'))
        return lambda url, *args: (*(t[url] if url in t else args), url)

    def __init__(self, root, w, h, rows, font, grid, translator, langs, dest, temp, skip_video=False, no_ow=False,
                 print_progress=False):
        self.langs, self.dest, self.temp = langs, dest, temp
        self.dl_params = dest, temp, langs, skip_video, no_ow

        self.frame = Frame(root)
        self.frame.grid(**grid)

        row_height = font.metrics('linespace')
        super().__init__(self.frame, w, h - 2 * row_height, rows, ('title', 'artist', 'id'), {})

        self.restricted_letters = '<>/\\"”\':|?*'

        self.trans_file = translator
        self.translator = self.get_translator(translator)
        self.id_table = {}
        self.running, self.downloaded = [], []

        self.table.bind("<Return>", self.download_selection)
        self.table.bind("<Button-3>", self.edit)

        self.print_progress = print_progress
        self.root.after(100, self.check_finished)

        dl = Button(self.frame, text='download all', command=lambda: [self.mp_dl(iid) for iid in self.id_table])
        st = Button(self.frame, text='stop downloads', command=self.cancel_dl)

        dl.pack(), st.pack()
        self.frame.update_idletasks()
        dl.pack_forget(), st.pack_forget()

        for i, b in enumerate((dl, st)):
            if b.winfo_width() > w[1]:
                b.pack(side='bottom')
            elif i:
                b.pack(side='right')
            else:
                b.pack(side='left')

    def on_edit(self, entries, args):
        (t, a, i), (_, _, url) = entries, args
        open(self.trans_file, 'a', encoding='utf-8').write(f'\n{url} : {t.get()} | {a.get()}')

    def add(self, index, values, tags=''):
        super().add(index, self.translator(values[-1], *values[:2]), tags)

    def check_finished(self):
        for i, p in self.running[:]:
            if p.is_alive():
                continue
            self.running.remove((i, p))
            url = self.id_table[i]
            self.table.tag_configure(url, background='green')
            self.downloaded.append(url)

        if self.print_progress:
            print(f'\rdownloading:{len(self.running):>3} | finished:{len(self.downloaded):>3}', end='')

        self.root.after(100, self.check_finished)

    def cancel_dl(self):
        for iid, process in self.running:
            if not process.is_alive():
                continue
            process.terminate()
            self.ignore.remove(iid)
            self.table.tag_configure(self.id_table[iid], background='white')
        self.running = []

    def mp_dl(self, iid):
        url = self.id_table[iid]
        self.table.tag_configure(url, background='grey')
        self.ignore.append(iid)

        args = self.table.item(iid)['values']
        if not all(args):
            return

        process = Process(target=self.download_video, args=(args, self.dl_params))
        self.running.append((iid, process))
        process.start()

    def download_selection(self, *_):
        iids = self.table.selection()
        for iid in iids:
            if iid in self.ignore:
                continue
            self.mp_dl(iid)
        self.table.selection_clear()
