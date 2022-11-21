from tkinter import Entry


class SearchBar:
    def __init__(self, root, results, grid, font):
        self.results = results
        self.entry = Entry(root, font=font, width=max(len(x) for x in results.searches))
        self.entry.grid(**grid)

        self.entry.bind('<Return>', self.search)

    def search(self, *_):
        self.results.add(self.entry.get())
        self.entry.delete(0, 'end')