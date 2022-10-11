import tkinter
import time
import datetime

FILE = 'to-do_list.txt'
all_tasks = [Task.from_file(a, i) for i, a in enumerate(open(FILE).read().split('\n\n'))]

class Task:
    def __init__(self, title, body, date, position):
        self.title, self.body = title, body
        self.position = position
    
    @classmethod
    def from_file(cls, string, index):
        """format:
        title\00body\00\date"""
        title, body, d, position = string.split('\00')
        d = datetime.date(*[int(e) for e in d.split('/')])
        return cls(title, body, d, position)

        
def write():
    open(FILE, 'w').write('\n\n'.join('\00'.join(t.info) for t in all_tasks))