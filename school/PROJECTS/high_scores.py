#!/usr/bin/python
# high_scores.py
__author__ = "Andrew Kornder"
__version__ = '2.0'

'''module to be used to handle highscores for a game, includes working
   with the display and management of data as well'''

from time import strftime
from tkinter import Tk
from tkinter.ttk import Treeview
from re import fullmatch
from os.path import exists


def _create_window(scores: list) -> tuple:
    """
    helper function for show_scores_GUI and option_menu.
    only used to create a basic window (not to be used from another file)

    :param scores: a list of scores to be displayed
    :return: None
    """

    root = Tk()
    root.configure(height=620, width=250)
    root.title('scores!')
    table = Treeview(root, columns=('pos', 'date', 'user', 'score', 'other'),
                     show='headings')

    for heading in table['columns']:
        table.heading(heading, text=heading.upper())
    for i, value in enumerate(scores):
        table.insert('', 'end', values=(f'{i + 1}.',) + value[2::-1] + (value[-1],))

    table.pack()

    return root, table


def _valid_file(path: str) -> bool:
    """
    simple helper function to validate file names using regex in change_file

    returns true if the file is in the format of:
        1. folder/file.txt
        2. C:/folder/sub-folder/file.txt
        3. file.txt

    :param path: a file path to be checked
    :return: bool value whether the file path is valid
    """

    # regex expression for paths in mac and windows (first time using regex so might not work)
    file_name_pattern = r'^([a-zA-Z]:[\\|\/])?([\w\- ]+[\\|\/])*([\w\- ]+\.(txt|pdf|doc|docx|xls|xlsx)){1}$'

    if not bool(fullmatch(file_name_pattern, path)):
        return False

    if not exists(path):  # try to create the file if it doesn't exist
        try:
            open(path, 'x')
        # in case the regex was wrong, and the file path wasn't valid, return false
        # this can also happen if it is syntactically correct, but the directory doesn't exist
        except IOError:
            return False
    return True


def _valid_sep(sep: str) -> bool:
    """
    simple helper function to validate separator using regex for change_sep

    conditions to be valid separator:
        - not alphanumeric
        - does not include underscores, whitespace, new line characters or periods
        - must be at least 1 character long

    :param sep: a separator to be checked
    :return: bool value whether the separator is valid
    """

    pattern = r'[^\w \n\.,\\]+'  # not alphanumeric and does not have '_', '\n', '.', ',' or ' '
    return bool(fullmatch(pattern, sep)) and bool(sep)  # adding 'not sep' makes sure it is at least one char long


class Scorekeeper:
    def __init__(self, file_name: str = 'default_scores.txt',
                 separator: str = '~', sortby: str = 'score',
                 default: tuple = ('0', 'John Smith', '1/1/1999', '')) -> None:
        """
        creates the object to keep track of data

        :param file_name: a file to be used as the record of scores
        :param separator: a delimiter between values in the file (not really useful for the user)
        :param sortby: "score" to sort values by scores, or "name" to sort by name
        :param default: a default score used whenever clearing data
        :return: None
        """

        self.file_name, self.separator, self.default = 'default_scores.txt', '~', separator.join(
            default)

        # setting sortby to be an index to be used in add_score()
        if sortby in ('name', 'score'):
            self.sortby = {'score': 0, 'name': 1}[sortby]
        else:
            raise Exception(f'{sortby} is not an accepted sorting method')

        # checking for valid strings before accepting the separator and file path
        self.change_file(file_name)
        self.change_sep(separator)

    def read_scores(self) -> list:
        """
        reads and formats the data from a
        file into a tuple, then returns those in a list

        :return: a list of tuples which show the score, name and date from each score
        """

        # splitting file into rows, then splitting each row into individual values
        return [tuple(a.split(self.separator)) for a in
                open(self.file_name).read().split('\n') if a != '']

    def show_scores(self) -> None:
        """
        reads and prints all the scores into the console

        :return: None
        """

        # retrieves value then adds new lines between them for readability
        print('\n'.join(map(', '.join, self.read_scores())))

    def add_score(self, user_score: int, user: str, *args) -> None:
        """
        adds a score to the list of highscores

        :param user_score: the score that the user achieved
        :param user: the username to be used in the highscore
        :return: None
        """

        data = self.read_scores()

        # find the index to insert the score with a list comp, adds len(data) in case the list comp is empty
        # then format the score and insert it into data
        data.insert(([i for i, score in enumerate(data) if
                      ((float(score[0]) < user_score) if not self.sortby else score[1] > user)] + [len(data)])[0],
                    [str(user_score), user, strftime('%x'), ', '.join(args)])

        # write the scores into the file with values separated by % and with new lines in between scores
        open(self.file_name, 'w').write(
            '\n'.join([self.separator.join(a) for a in data]))

    def clear_data(self, data: list = ()) -> None:
        """
        clears the data in a file and adds a user-curated set of values

        :param data: a list of strings to be used as the default data set once the data is wiped
        :return: None
        """

        # opens the file and then adds the single default value, unless the user added a list of entries
        # if so, formats then adds those
        open(self.file_name, 'w').write(self.default if not data else '\n'.join(
            [self.separator.join(a) for a in data]))

    def remove_user(self, name: str) -> None:
        """
        removes a user's scores from a file

        :param name: the name to be searched and deleted
        :return: None
        """

        # searches through data to find all values with the param name in it
        # then removes them and rewrites the file
        data = self.read_scores()
        open(self.file_name, 'w').write(
            '\n'.join([self.separator.join(score) for score in
                       data if name != score[1]]))

    def no_defaults(self) -> None:
        self.delete_score(self.default.split(self.separator))

    def delete_score(self, value: list | tuple) -> list:
        """
        finds a value and deletes it from the list of scores as well as all matching values.

        :param value: the tuple holding the values in the score
        :return: a list of the indices that were deleted
        """

        # get date from the file and compare line by line the scores
        data, score = open(self.file_name, 'r').read().split(
            '\n'), self.separator.join(value)
        indices = [i for i, entry in enumerate(data) if entry == score]

        # after grabbing the indices for deletion, delete them and return the indices
        open(self.file_name, 'w').write(
            '\n'.join([e for i, e in enumerate(data) if i not in indices]))
        return indices

    def option_menu(self) -> None:
        """
        creates a window that shows scores and lets the user
        delete a certain user's scores by clicking on them

        :return: None
        """

        def mouse_click(selections: tuple) -> None:
            children = display.get_children()
            for selected in selections:
                # finding which score was selected, then removing that value
                _, date, name, score, opts = display.item(selected)['values']
                for i in self.delete_score((str(score), name, date, opts)):
                    display.delete(children[i])

        root, display = _create_window(self.read_scores())
        display.bind('<<TreeviewSelect>>',
                     lambda _: mouse_click(display.selection()))

        root.mainloop()

    def change_sortby(self):
        self.sortby = not self.sortby; self._sort_values()

    def _sort_values(self):
        """sorts all values by name or score depending on self.sortby"""

        self.no_defaults()
        data = self.read_scores()
        open(self.file_name, 'w').write(
            '\n'.join([self.separator.join(a) for a in sorted(data, key=lambda x: x[self.sortby])]))

    def show_scores_GUI(self) -> None:
        """
        creates a window that shows scores using a tkinter.ttk.treeview widget.

        :return: None
        """

        _create_window(self.read_scores())[0].mainloop()

    def change_file(self, new_file: str) -> None:
        """
        change the file that the Scorekeeper is writing to

        :param new_file: a valid path/file name of any file that is writeable
        :return: None
        """

        if _valid_file(new_file):
            self.file_name = self.file_name
        else:
            raise Exception(f'"{new_file}" was not found to be a valid file.')

    def change_default_value(self, new_default: tuple | list) -> None:
        """
        change the default attribute, which is used in

        :param new_default: an iterable that holds 3-4 values (score, name, date, *optional values*)
        :return: None
        """

        # first checking the length of the list, then the individual lengths of the values
        if 2 < len(new_default) < 5 and all(new_default):
            self.default = self.separator.join(new_default)
        else:
            raise Exception(f'{new_default} is not a valid default value')

    def change_sep(self, new_sep: str) -> None:
        """
        change the way the data is stored (try not to choose common characters,
        as it will replace those that already exist in usernames or scores)

        :param new_sep: a character or string that will be used to separate values in the file
        :return: None
        """

        if not _valid_sep(new_sep):
            raise Exception(
                f'"{new_sep}" was not found to be a valid separator')

        # replacing the existing separators
        text = open(self.file_name).read()
        open(self.file_name, 'w').write(text.replace(self.separator, new_sep))

        self.separator, self.default = new_sep, self.default.replace(
            self.separator, new_sep)


if __name__ == '__main__':
    from random import sample

    # testing _valid_file and _valid_sep
    paths = ['c:/folder/fo -%/file.txt', 'c:/', 'c:/folder/file.txt',
             'Folder/file.tx', 'Folder/file.txt', 'file.txt', 'file.asda'
                                                              '*&!@#^', r'\n.txt', 'abc.abc', '', 'file', '']
    print('_valid_file\n' + ''.join(f'\n{_valid_file(a)} for "{a}"' for a in paths), '\n\n')

    seps = [' ', 'x', 'a', 'ABC', '$', '~', '', '_', r'\n']
    print('_valid_sep\n' + ''.join(f'\n{_valid_sep(a)} for "{a}"' for a in seps))

    # testing the methods of Scorekeeper
    t = Scorekeeper()
    t.clear_data()

    words = [''.join(sample('abcdefghijklmnopqrstuvwxyz', 6)) for _ in
             range(100)]
    test = sample(range(500), 100)
    for j, k in zip(test, words):
        t.add_score(int(j), k)

    t.option_menu()
    t.change_sortby()
    t.option_menu()
