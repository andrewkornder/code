import random as r
import timeit


def insertion_sort(l):
    comps = 0
    for i, e in enumerate(l):
        for idx, element in enumerate(l[:i]):
            comps += 1
            if element > e:
                l.insert(idx, e)
                del l[i + 1]
                break

    return l


def counting_sort(l):
    nl = [None] * max(l)
    fl = []
    for a in l:
        nl[a - 1] = a

    for a in nl:
        if a is not None:
            fl.append(a)
    return fl


def radixLSD_sort(l):
    maxn = max(l)
    maxlen = len(str(maxn))
    bucks = {i: [] for i in range(10)}
    for i, n in enumerate(l):
        s = str(n)
        s = '0' * (maxlen - len(s)) + s
        d = int(s[-1])
        bucks[d].append(n)

    for lsd in range(2, maxlen + 1):
        for last_d, bucket in bucks.items():
            for n in bucket[:]:
                s = str(n)
                s = '0' * (maxlen - len(s)) + s
                d = int(s[maxlen - lsd])
                bucket.remove(n)
                bucks[d].append(n)

    l = []
    for b in bucks.values():
        if not b:
            continue
        if any([a > b[i + 1] for i, a in enumerate(b[:-1])]):
            b = insertion_sort(b)
        l += b

    return l


def bucket_sort(unordered_list):
    ln = len(unordered_list)
    unordered_list = [a / 1000 for a in
                      r.sample(range(0, len(unordered_list)), ln)]
    buckets = [[None] for _ in range(10)]
    l = []
    for ele in unordered_list:  # assuming numbers are all postive floats
        n = int(ele * 10) - 1
        buckets[n].append(ele)

    for b in buckets:
        l += insertion_sort(b[1:])

    return l


def bubble_sort(unordered_list):
    c = True
    it = 0
    comps = 0
    m = len(unordered_list) - 1
    while c:
        it += 1
        c = False
        for i, e in enumerate(unordered_list):
            comps += 1
            if i == m:
                break
            ni = i + 1
            n = unordered_list[ni]
            comps += 1
            if e > n:
                if not c:
                    c = True
                unordered_list[ni] = e
                unordered_list[i] = n

    return unordered_list


def binary_search(sorted_list):
    target = r.choice(sorted_list)
    _, iterations = bs_helper(sorted_list, target, 0, len(sorted_list))


def bs_helper(l, e, start=0, stop=None, c=0):
    if stop is None:
        stop = len(l)

    i = int((start + stop) / 2)
    t = l[i]
    if t == e:
        return i, c
    if t > e:
        return bs_helper(l, e, start, i, c + 1)
    return bs_helper(l, e, i, stop, c + 1)


def selection_sort(unordered_list):
    l = len(unordered_list)
    c = 0
    while c != l:
        m = unordered_list[-1], l - 1
        for i, a in enumerate(unordered_list):
            if i < c:
                continue
            if a < m[0]:
                m = a, i
        del unordered_list[m[1]]
        unordered_list.insert(c, m[0])
        c += 1

    return unordered_list[:l]


def bogo_sort(l):
    while any([a > l[i + 1] for i, a in enumerate(l[:-1])]):
        l = r.sample(l, len(l))
    return l


def test_search(func, length, test=False):
    l = sorted(r.sample(range(0, length + 2), length))
    t = r.choice(l)

    if not test:
        print('target: {0} in a list of length {1} using {2}'.format(t, length,
                                                                     str(func).split()[
                                                                         1]))
    index, count = func(l, t, 0, length - 1, 0)
    if not test:
        print('found at index: {0} with {1} iterations'.format(index, count))
    return count


def test_sort(func, length, test=False):
    l = r.sample(range(0, length + 2), length)
    if not test:
        print('list: {0} \nwith {1} items using {2}'.format(l, length,
                                                            str(func).split()[
                                                                1]))
    start = timeit.default_timer()
    result = func(l[:])
    end = timeit.default_timer() - start
    if not test:
        if len(result) == 3 and result[2] != []:
            sl, count, comp = result
            print(
                '\nsorted: {0} \nused {1} iterations with {2} comparisons'.format(
                    sl, count, comp))
        else:
            print('\nsorted: {0} \nused {1} iterations'.format(result[0],
                                                               result[1]))
    if any([a not in result[0] for a in l]):
        print('failed test')
    return result, end
