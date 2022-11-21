from os import remove, listdir, mkdir, system
from os.path import exists
from tkinter.font import Font
from tkinter import Tk

from editable_list import DownloadList
from search_bar import SearchBar
from search_results import SearchResults


class Display:
    def __init__(self, w, h, consts, translator=None, auto=False, open_destination=False, first_k=None):
        destination, read, temp, langs, past = consts

        for subfolder in ('subtitles', 'thumbnails', 'mp3s'):
            folder = f'{destination}/{subfolder}'
            if not exists(folder):
                mkdir(folder)

        for lang in langs:
            folder = f'{destination}/subtitles/{lang}'
            if not exists(folder):
                mkdir(folder)

        self.queries = open(read, encoding='utf-8').read().split('\n')
        if first_k:
            self.queries = self.queries[:first_k]

        self.root = Tk()
        self.root.resizable(False, False)
        self.root.title('Downloader')
        self.root.geometry(f'{w}x{h}')

        self.font = Font(family='Niagara Bold', size=10)
        list_width = min(self.font.measure(max(self.queries + ['abcdefgh'], key=len)), w // 8)

        self.w, self.h = w, h

        row_height = h - 50

        info = DownloadList(self.root, w=list_width, h=row_height, rows=len(self.queries),
                            grid={'row': 0, 'column': 0, 'columnspan': 2}, translator=translator,
                            dest=destination, temp=temp, langs=langs)
        search = SearchResults(self.root, w - list_width * 3 - 10, row_height, length=3, title_font=self.font,
                               tree=info, grid={'row': 0, 'column': 2}, searches=self.queries, auto=auto, temp=temp,
                               past=past)
        search.search()

        SearchBar(self.root, search, {'row': 1, 'column': 2})

        # self.root.mainloop()

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
    Display(1700, 600, (_destination, _read, _temp, _langs, _past), translator=_translator,
            auto=False, open_destination=False, first_k=None)
