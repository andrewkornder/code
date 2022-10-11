import datetime as dt
import time as t


def double(word):
    counts = {count: {'c': 0, 'p': []} for pos, count in enumerate(word)}
    for pos, l in enumerate(word):
        counts[l]['c'] += 1
        counts[l]['p'].append(pos)
    doubles = {d: {'c': c['c'], 'p': c['p']} for d, c in counts.items() if
               c['c'] > 1}
    return doubles


def check(guess1, words_original0):
    doubled = double(guess1[0])
    guessA = guess1[1]
    guessL = guess1[0]
    blist = [b for i, b in enumerate(guessL) if
             guessA[i] == 'b' and b not in doubled]
    glist = {pos: g for pos, g in enumerate(guessL) if
             guessA[pos] == 'g' and g not in doubled}
    ylist = {pos: y for pos, y in enumerate(guessL) if
             guessA[pos] == 'y' and y not in doubled}
    final = words_original0[:]
    for b in blist:
        final = [word for word in final if b not in word]
    for p, g in glist.items():
        final = [word for word in final if word[p] == g]
    for p, y in ylist.items():
        final = [word for word in final if word[p] != y and y in word]
    for word0 in final:
        word = list(word0)
        for d in doubled.items():
            currL = d[0]
            for p in d[1]['p']:
                currA = p
                for l in word0:
                    if currA == 'g':
                        if currL != l:
                            final.remove(word0)
                            break
                        word.remove(l)
                        continue
                    if currA == 'y':
                        if currL == l or l not in word:
                            final.remove(word0)
                            break
                        word.remove(l)
                        continue
                    else:
                        if l in word:
                            word.remove(l)
                            break
    if guessL in final:
        final.remove(guess1[0])
    return final, len(words_original0) - len(final)


def test(words):
    if len(words) == 1:
        return words
    start = t.time()
    best_words = {}
    for word in words:
        score = 0
        for perm in [check_guess(word, ans) for ans in words]:
            removed = check([word, perm], words)[1]
            score += removed
        while score in best_words:
            score -= 1
        best_words[score] = word
    scores = list(best_words.keys())
    scores.sort()
    scores.reverse()
    words2 = [best_words[score] for score in scores]
    # print(words2, 'in test()')
    return words2


def play(finalword, i, filename):
    print(str(i + 1) + '. ' + finalword)
    turns = 0
    words = all_words[:]
    best = 'salet'
    while True:
        turns += 1
        if best == finalword:
            with open(filename, 'a') as file:
                file.write('\n' + str(
                    i + 1) + '. ' + finalword + '\n\tsolved ' + finalword + ' in ' + str(
                    turns) + ' turns')
            if turns > 6:
                print('🟢🟢🟢🟢🟢')
                return turns, finalword
            print('🟢🟢🟢🟢🟢')
            return turns, ''
        ca = check_guess(best, finalword)
        print(colors(ca))
        words = test(check([best, ca], words)[0])
        best = words[0]


def colors(ans):
    colors = {
        'b': '\u26AB',
        'g': '🟢',
        'y': '🟡'}
    color_lists = ''.join(map(str, [colors[a] for a in ans]))
    return color_lists


def check_guess(guess, ans):
    info = [' '] * 5
    word, answer = list(guess), list(ans)

    for i, e in enumerate(word):
        if e == answer[i]:
            info[i] = 'g'
            answer[i] = ' '

    for i, e in enumerate(word):
        if info[i] != ' ':
            continue

        if e in answer:
            info[i] = 'y'
        else:
            info[i] = 'b'
        answer[i] = ' '

    return info


def count_letters(word):
    counts = {count: 0 for count in word}
    for l in word:
        counts[l] += 1
    return counts


def runtests():
    date = str(dt.datetime.now()).split('.')[0].replace(':', '.')
    filename = 'answers ' + date + '.txt'
    f = open(filename, "x")
    f.close()
    st = t.time()

    with open(filename, 'w') as file:
        file.write('SOLVED\n====================================')

    all_returns = [play(word, i, filename) for i, word in enumerate(all_words)]
    stop = t.time() - st
    with open(filename, 'a') as file:
        file.write('\non average each test took ' + str(
            stop / len(all_returns)) + ' seconds for a total time of ' + str(
            stop) + str(('%H:%M:%S', t.gmtime(stop))))
    with open('times.txt', 'a') as file:
        file.write(filename.split()[1] + '\'s time: ' + str(
            stop) + 's\n------DONE------\n')
    scores = [curr[0] for curr in all_returns if curr[1] == '']
    failed = [curr[1] for curr in all_returns if curr[1] != '']
    total = 0
    for s in scores:
        total += s
    total = total / len(scores)
    with open(filename, 'a') as file:
        file.write('\naverage turns to win: ' + str(total) + '\n' + ', '.join(
            map(str, failed)))
    print('----done----')
    input()
    exit()


def word_lists():
    words = open('words.txt').read().split('\n')
    all_poss = words[0].split(',')
    all_words = words[1].split(',')
    return all_poss, all_words


def score_round(word, all_w):
    perms = [check_guess(word, ans) for ans in all_w]
    for p in perms:
        left, score = check([word, p], all_w)
    return score, left


def test2(words):
    scores = {word: 0 for word in words}
    for word in words:
        left = score_round(word, words)[1]
        total = 0
        for l in left:
            score = score_round(l, left)[0]
            total += score
        while total in scores.values():
            total -= 1
        scores[word] = total
    new_list = list(scores.values())
    new_list.sort(reverse=True)
    dct = {v: k for k, v in scores.items()}
    new_list = [dct[score] for score in new_list]
    return new_list


def get_ans():
    words = all_words[:]
    best = 'salet'
    answers = []
    while True:
        user = input('guess: ').split()
        if user == 'restart':
            get_ans()
        if len(user) == 2:
            answers.append(user[1])
            words = check(user, words)[0]
        elif len(user) == 1:
            answers.append(user[0])
            words = check([best, user[0]], words)[0]
        # colors(answers)
        x = test(words)
        if len(words) == 0:
            print('failed getting any words')
            continue
        words = x
        best = words[0]
        print(len(words), 'words:', ', '.join(map(str, words)))
        print(best)


global all_words
global all_poss
all_poss, all_words = word_lists()
with open('times.txt', 'a') as file:
    file.write('TIMES\n====================================\n')
if __name__ == '__main__':
    print(test(all_words))
    get_ans()
