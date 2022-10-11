def score(word, answer):
    info = ['b', 'b', 'b', 'b', 'b']

    answer = list(answer)
    for i, e in enumerate(word):
        if e == answer[i]:
            info[i] = 'g'
            answer[i] = ' '

    for i, e in enumerate(word):
        if e in answer:
            info[i] = 'y'
            answer[answer.index(e)] = ' '

    return info


def start():
    return open('answers.txt').read().split('","')


with open('precomputed.txt', 'w') as pc:
    a = start()
    pc.write(','.join(a) + '\n')

    pc.write('\n'.join([','.join([''.join(score(word, comb)) for comb in a]) for word in a]))
