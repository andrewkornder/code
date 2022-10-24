zl = open('guesses.txt').read().split('\n')
answers = []
length = len(zl)


def elim_collisions(guess, words):
    return [w for w in words if not any(l in guess for l in w)]


for i, a in enumerate(zl):
    al = elim_collisions(a, zl)
    for j, b in enumerate(al):
        bl = elim_collisions(b, al)
        for c in bl:
            cl = elim_collisions(c, bl)
            for d in cl:
                answers.extend((a, b, c, d, e) for e in elim_collisions(d, cl))

        print(f'\r{(i + j / len(al))/ length * 100:>10.4f}%', end='')
print('', *answers, sep='\n')