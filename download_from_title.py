s, t = __import__('youtubesearchpython').VideosSearch, open('to_download').read().split('\n')
results = list(map(lambda q: s(q, limit=1).result()['result'][0], t))

from pprint import pprint
from os import system
info = {video['id']: video['title'] for video in results}
pprint(info)

while input('?'):
    for (k, v), q in zip(info.items(), t):
        if input(v):
            r = s(q, limit=3).result()['result']
            print('\n'.join(map(lambda x: x['title'], r)))
            info[k] = r[int(input())]['id']


map(lambda x, _: system(f'youtube-dl {x}'), info.items())
print('done')
