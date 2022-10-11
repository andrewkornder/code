import time
import tkinter


def read_scores(file):
    """
    reads and formats the data from a
    file into a tuple, then returns those in a list

    :param file: the path or name of a file to pull data from
    :return: a list of tuples which show the score, name and date from each score
    """

    # splitting file into rows, then splitting each row into individual values
    return list(map(lambda a: a.split('%') if a != ''
                    else ['0', '1/1/1999'], open(file, 'r').read().split('\n')))


def show_scores(file):
    """
    reads and prints all the scores into the console

    :param file: the path or name of a file to pull data from
    :return: None
    """

    # retrieves value then adds new lines to them for readability
    print('\n'.join(map(' '.join, (read_scores(file)))))


def add_score(file, user_score, *args):
    """
    adds a score to the list of highscores

    :param file: the path or name of a file to add the score to
    :param user_score: the score that the user achieved
    :return: None
    """

    entry = [str(user_score), time.strftime('%x')]
    data = read_scores(file)
    open(file, 'w').write('\n'.join(['%'.join(a) for a in data + [entry]]))


def clear_data(file):
    """
    clears the data in a file

    :param file: the path or name of a file to clear
    :return: None
    """

    # opening file as 'w' overwrites the data, and not saving the file in a var
    # results in it being garbage collected, so no file.close() is needed
    open(file, 'w')


def remove(file, part):
    """
    removes a user's scores from a file

    :param file: the path or name of a file to be edited
    :param part: the part of the score to be searched and deleted
    :return: None
    """

    data = read_scores(file)
    open(file, 'w').write('\n'.join(['%'.join(score) for score in data if
                          part not in score]))


def show_scores_GUI(file):
    """
    creates a window that shows scores

    :param file: the path or name of a file to grab scores from
    :return: None
    """

    root = tkinter.Tk()
    root.title("")
    root.geometry('150x50')
    score = [int(a[0]) for a in read_scores(file)]
    lb = tkinter.Label(root, width=18,
                       text='average score: {}'.format(round(sum(score) / len(score), 3)))
    lb.pack()

    root.mainloop()
