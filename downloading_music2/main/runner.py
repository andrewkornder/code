from os import mkdir, system, path
from shutil import rmtree
from tkinter.font import Font
from tkinter import Tk

from editable_list import DownloadList
from search_results import SearchResults


class Display:
    def __init__(self, w: int, h: int, consts: tuple[str, str, str, list[str], str], translator: None | str = None,
                 auto: bool = False, first_k: None | int = None, skip_video: bool = False, overwrite: bool = True,
                 wipe_prev: bool = False, strict_prev: bool = False) -> None:
        (self.destination, self.read, self.temp, self.langs, self.past), self.translator = consts, translator

        def check_folder(folder):
            if not path.exists(folder):
                mkdir(folder)

        if wipe_prev:
            rmtree(self.destination)

        check_folder(self.destination)
        check_folder(self.temp)

        [check_folder(f'{self.destination}/{subfolder}') for subfolder in
         ('thumbnails', 'thumbnails/original', 'thumbnails/square',
          'subtitles', [f'subtitles/{la}' for la in self.langs])
         + (('mp3s',) if not skip_video else ())]

        self.queries = open(self.read, encoding='utf-8').read().split('\n')
        if first_k:
            self.queries = self.queries[:first_k]

        self.root = Tk()
        self.root.resizable(False, False)
        self.root.title('Downloader')
        self.root.geometry(f'{w}x{h}')

        self.font = Font(family='Niagara Bold', size=10)
        lw = (lambda x: [x, 2 * x // 3, 2 * x // 5])(min(self.font.measure(max(self.queries +
                                                                               ['abcdefgh'], key=len)), w // 8))
        self.w, self.h = w, h

        self.info = DownloadList(self.root, w=lw, h=h, rows=len(self.queries), font=self.font,
                                 grid={'row': 0, 'column': 0}, translator=translator,
                                 dest=self.destination, temp=self.temp, langs=self.langs,
                                 skip_video=skip_video, no_ow=not overwrite)

        self.search = SearchResults(self.root, w - sum(lw) - 10, h, length=3, title_font=self.font,
                                    tree=self.info, grid={'row': 0, 'column': 2}, searches=self.queries,
                                    auto=auto, temp=self.temp, past=self.past, strict_prev=strict_prev)

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

        open(self.past, 'w', encoding='utf-8').write('\n'.join(past_items))

        rmtree(self.temp)

        if open_destination:
            system('start ' + self.destination)


class Selector:
    def __init__(self, cls):
        params, types = zip(*cls.__init__.__annotations__.items())
        types = [help(t) if type(t) != type else t for t in types]
        print(*types, sep='\n')


if __name__ == '__main__':
    _destination = 'C:/Users/Administrator/OneDrive/Desktop/folders/music'
    _read = './utils/to_download.txt'
    _temp = './utils/temp'
    _langs = ['en', 'ja']
    _past = './utils/past_saves.txt'
    _translator = './utils/translator.txt'

    _sp = True
    _au = False
    _od = True
    _fk = None
    _sk = False
    _ov = False
    _wp = False

    Selector(Display)
    exit()
    Display(1700, 600, (_destination, _read, _temp, _langs, _past), translator=_translator, strict_prev=_sp, auto=_au,
            first_k=_fk, skip_video=_sk, overwrite=_ov, wipe_prev=_wp).run(open_destination=_od)
