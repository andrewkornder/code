from os import remove, listdir, mkdir, system
from os.path import exists
from shutil import rmtree
from tkinter.font import Font
from tkinter import Tk

from editable_list import DownloadList
from search_results import SearchResults


class Display:
    def __init__(self, w, h, consts, translator=None, auto=False, open_destination=False, first_k=None,
                 skip_video=False, overwrite=True, wipe_prev=False, strict_prev=False):
        destination, read, temp, langs, past = consts

        def check_folder(folder):
            if not exists(folder):
                mkdir(folder)

        if wipe_prev:
            rmtree(destination)
        check_folder(destination)

        [check_folder(f'{destination}/{subfolder}') for subfolder in
         ('thumbnails', 'thumbnails/original', 'thumbnails/square', 'subtitles', [f'subtitles/{la}' for la in langs])
         + (('mp3s',) if not skip_video else ())]

        self.queries = open(read, encoding='utf-8').read().split('\n')
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

        info = DownloadList(self.root, w=lw, h=h, rows=len(self.queries), font=self.font,
                            grid={'row': 0, 'column': 0}, translator=translator,
                            dest=destination, temp=temp, langs=langs, skip_video=skip_video, no_ow=not overwrite)
        search = SearchResults(self.root, w - sum(lw) - 10, h, length=3, title_font=self.font,
                               tree=info, grid={'row': 0, 'column': 2}, searches=self.queries, auto=auto, temp=temp,
                               past=past, strict_prev=strict_prev)
        search.search()

        self.root.mainloop()

        trans = {a: b for a, b in [tuple(x.split(' : ')) for x in
                 filter(bool, open(translator, encoding='utf-8').read().split('\n'))]}
        open(translator, 'w', encoding='utf-8').write('\n'.join(map(' : '.join, trans.items())))

        past_items = {a for a in open(past, encoding='utf-8').read().split('\n')}
        for i in range(len(search.searches)):
            if i not in search.chosen:
                continue

            video = search.results[i][search.chosen[i]]
            if video['id'] not in info.downloaded:
                continue

            past_items.add(f'{video["title"]} | {video["id"]}')

        open(past, 'w', encoding='utf-8').write('\n'.join(past_items))

        for file in listdir(temp):
            remove(f'{temp}/{file}')

        if open_destination:
            system('start ' + destination)


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

    Display(1700, 600, (_destination, _read, _temp, _langs, _past), translator=_translator, strict_prev=_sp, auto=_au,
            open_destination=_od, first_k=_fk, skip_video=_sk, overwrite=_ov, wipe_prev=_wp)
