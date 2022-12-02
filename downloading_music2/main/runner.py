#!/usr/bin/python
# runner.py
__author__ = "Andrew Kornder"
__version__ = '1.0'


from os import mkdir, system, path, listdir, name as os_name
from shutil import rmtree
from tkinter.font import Font
from tkinter import Tk

from editable_list import DownloadList
from search_results import SearchResults


class Display:
    def __init__(self, w_h_r: float, consts: tuple[str | tuple[str] | list[str], str, str, list[str], str],
                 first_k: None | int = None, translator: None | str = None, auto: bool = False, wipe_prev: bool = False,
                 strict_prev: bool = False, print_progress: bool = False, skip_video: bool = False,
                 overwrite: bool = True, pages: int = 3):

        (self.destination, self.read, self.temp, self.langs, self.past), self.translator = consts, translator

        def check_folder(folder):
            if not path.exists(folder):
                mkdir(folder)

        if wipe_prev:
            if skip_video:
                [rmtree(folder) for folder in (f'{self.destination}/subtitles',
                                               f'{self.destination}/thumbnails') if path.exists(folder)]
            else:
                rmtree(self.destination)

        check_folder(self.destination)
        check_folder(self.temp)

        [check_folder(f'{self.destination}/{subfolder}') for subfolder in
         ('thumbnails', 'thumbnails/original', 'thumbnails/square',
          'subtitles', *[f'subtitles/{la}' for la in self.langs])
         + (('mp3s',) if not skip_video else ())]

        if isinstance(self.read, (list, tuple)):
            self.queries = list(self.read)
        else:
            self.queries = open(self.read, encoding='utf-8').read().split('\n')

        if first_k:
            self.queries = self.queries[:first_k]

        self.root = Tk()
        self.root.resizable(False, False)
        self.root.title('Downloader')
        self.w, self.h = (lambda d: (d - 2, int(d / w_h_r) - 1))(self.root.winfo_screenwidth())
        self.root.geometry(f'{self.w}x{self.h}+0+0')

        self.font = Font(family='Niagara Bold', size=10)
        lw = (lambda x: [x, 2 * x // 3, 2 * x // 5])(min(self.font.measure(max(self.queries + ['abcdefgh'],
                                                                               key=len)), self.w // 8))

        self.info = DownloadList(self.root, w=lw, h=self.h, rows=len(self.queries), font=self.font,
                                 grid={'row': 0, 'column': 0}, translator=translator,
                                 dest=self.destination, temp=self.temp, langs=self.langs,
                                 skip_video=skip_video, no_ow=not overwrite, print_progress=print_progress)

        self.search = SearchResults(self.root, self.w - sum(lw) - 10, self.h, length=3, title_font=self.font,
                                    tree=self.info, grid={'row': 0, 'column': 2}, searches=self.queries,
                                    auto=auto, temp=self.temp, past=self.past, strict_prev=strict_prev, pages=pages)

    def run(self, open_destination=False):
        self.search.search()

        self.root.mainloop()

        trans = {a: b for a, b in [tuple(x.split(' : ')) for x in
                                   filter(bool, open(self.translator, encoding='utf-8').read().split('\n'))]}
        open(self.translator, 'w', encoding='utf-8').write('\n'.join(map(' : '.join, trans.items())))

        past_items = {a for a in open(self.past, encoding='utf-8').read().split('\n')}
        for i in range(len(self.search.searches)):
            if i not in self.search.chosen:
                continue

            video = self.search.results[i][self.search.chosen[i]]
            if video['id'] not in self.info.downloaded:
                continue

            past_items.add(f'{video["title"]} | {video["id"]}')

        # sorted bc sets are unordered, and I want it to only change the file if a change has actually been made
        open(self.past, 'w', encoding='utf-8').write('\n'.join(sorted(past_items)))

        rmtree(self.temp)

        if open_destination:
            system(('open ' if os_name == 'posix' else 'start ') + self.destination)


class Selector:
    def __init__(self, cls):
        self.params, self.types = zip(*cls.__init__.__annotations__.items())
        self.none = [any(str(x) == 'None' for x in str(t).split(' | ')) if '|' in str(t) else False for t in self.types]

        self.wrappers = list(map(lambda t: (lambda rep, lk=(lambda n: globals()['__builtins__'].__dict__[n]):
        (lambda wr, string: lambda x: wr([f(a) for f, a in zip([(lambda a, b: lambda _x: lk(a)(map(lk(b[:-1]), _x)))
        (*_t.split('[')) if '[' in _t else lk(_t) for _t in string.split(', ')], x)]))(rep[:-1].split('[')[0], '['.join(
        rep[:-1].split('[')[1:])) if '[' in rep else ([lk(x) for x in rep.split(' | ') if str(x) != 'None'][0] if '|'
        in rep else rep))(str(t)), self.types))


def rf(f0, ignored=(), lens=()):
    lens = list(lens)
    for f1 in listdir(f0):
        if f1 in ignored:
            continue
        fp = f'{f0}/{f1}'
        if path.isdir(fp):
            lens = rf(fp, ignored, lens)
        elif f1[-3:] == '.py':
            lens.append((f1, sum(c == '\n' for c in open(fp, encoding='utf-8').read())))
    return lens


if __name__ == '__main__':
    _destination = '/Users/akornder25/Documents/GitHub/folders/music/' if os_name == 'posix' else \
        'C:/Users/Administrator/OneDrive/Desktop/folders/music/'
    _read = './utils/to_download.txt'
    _temp = './utils/temp'
    _langs = ['en', 'ja']
    _past = './utils/past_saves.txt'
    _translator = './utils/translator.txt'

    _wh = 1700 / 600

    _pa = 5
    _sp = False
    _au = False
    _fk = None
    _sk = False
    _ov = False
    _wp = False
    _pr = True
    _od = True

    print(
        (lambda m: (lambda msg: (lambda width: (f'╔{"═" * width}╗\n' + ''.join(f'║{m: ^{width}}║\n' for m in msg) +
                    f'╚{"═" * width}╝'))(max(map(len, msg)) + 2))(list(map(lambda a: f"{f'%s : %s' % a}", m))) +
         f'\n{sum(x[1] for x in m)} lines of code')(rf("E:/code", ignored=("utils", "venv", 'py311')))
    )
    exit()
    Display(
        _wh,
        (
            _destination,
            _read,
            _temp,
            _langs,
            _past
        ),
        translator=_translator,
        first_k=_fk,
        pages=_pa,
        strict_prev=_sp,
        auto=_au,
        skip_video=_sk,
        overwrite=_ov,
        wipe_prev=_wp,
        print_progress=_pr
    ).run(
        open_destination=_od
    )
