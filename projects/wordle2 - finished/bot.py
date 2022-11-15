from time import time


def score(word, answer):
    info = ['b', 'b', 'b', 'b', 'b']

    word, answer = list(answer), list(word)
    for i, e in enumerate(word):
        if e == answer[i]:
            info[i] = 'g'
            answer[i] = ' '

    for i, e in enumerate(word):
        if info[i] != 'b':
            continue

        if e in answer:
            info[i] = 'y'
            answer[answer.index(e)] = ' '

    return info


def test(words):
    results = {}
    
    s = len(words)
    for word in words:
        results[word] = sum(s - len(remove_words(word, score(word, comp), words)) for comp in words[:])
    sorted_results = sorted(results.items(), key=lambda x: x[1])
    
    return list(map(lambda a: a[0], sorted_results[::-1]))


def remove_words(guess, info, words):
    l = [word for word in words if score(word, guess) == info]
    return l


def remove_words_v2(guess, info, words, testing=False):
    nw = words[:]
    gl, yl, bl = [], [], []
    for i, (v, l) in enumerate(zip(info, guess)):
        {'g': gl, 'y': yl, 'b': bl}[v].append((l, i))

    for letter, index in gl:
        for word in nw[:]:
            if letter != word[index]:
                nw.remove(word)
    for letter, index in bl:
        for word in nw[:]:
            if letter in word:
                nw.remove(word)
    for letter, index in yl:
        for word in nw[:]:
            if letter == word[index] or letter not in word:
                nw.remove(word)
    if testing:
        return len(words) - len(nw)
    return nw


def game(l):
    best = 'crane'
    while True:
        user = input('guess: ')
        if ' ' in user:
            guess, colors = user.split()
        else:
            colors = user
            guess = best
        if user == 'done':
            return
        l = test(remove_words(guess, list(colors), l))
        print(l)
        best = l[0]
        print(f'best word is {best}')


def average_score(words):
    total = 0
    start = time()
    for target in words:
        turns = 1
        l = words[:]
        best = 'salet'
        while best != target:
            l = test(remove_words(best, score(best, target), l))
            best = l[0]
            turns += 1
        total += turns
    open('average_score_1.0.txt', 'a').write(f'\n{total / len(words)} in {time() - start} seconds')


def start(): return open('answers.txt', 'r').read().split('\n')


if __name__ == '__main__':
    answers = start()
    print(answers[0])
    while True:
        game(answers[:])
