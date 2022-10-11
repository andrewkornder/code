from functools import cache
from math import isqrt, sqrt, prod, factorial
from itertools import permutations


def _get_factors(n):
    return sum(1 if n % i == 0 else 0 for i in range(2, isqrt(n) + 1))


@cache
def _fib(n):  # starting the fib series from 1, 2 instead of 0, 1
    if n <= 2:
        return n

    return _fib(n - 1) + _fib(n - 2)


def _is_prime(n):
    if n in (2, 3):
        return True

    if n % 6 not in (1, 5):
        return False

    if (2 ** n - 2) % n:
        return False

    for factor in range(2, isqrt(n) + 1):
        if n % factor == 0:
            return False

    return True


def p1(n):
    return sum(a for a in range(3, n, 1) if not a % 3 or not a % 5)


def p2(n):
    t = 0
    for i in range(1, n):
        f = _fib(i)
        if f > n:
            return t
        if f % 2 == 0:
            t += f


def p3(n):
    return max(factor for factor in range(2, isqrt(n) + 1) if n % factor == 0 and _is_prime(factor))


def p4(n):
    l = 0
    for i in range(10 ** n):
        for j in range(10 ** n):
            ij = i * j
            if ij > l and str(ij) == str(ij)[::-1]:
                l = ij
    return l


def p5(n):
    d = list(range(1, n))
    for c in range(n, 1 << 32, n):
        if all(c % div == 0 for div in d):
            return c


def p6(n):
    return sum(range(1, n + 1)) ** 2 - sum((a + 1) ** 2 for a in range(n))


def p7(n):
    n -= 5
    for x in range(13, 1 << 32, 2):
        if _is_prime(x):
            n -= 1
        if not n:
            return x


def p8(n, s):
    xs = [list(map(int, n[i:i + s])) for i in range(len(n))]
    print(xs)
    return max(prod(x) for x in xs)


def p9(n):
    for a in range(1, n):
        for b in range(a, n):
            c = sqrt(a ** 2 + b ** 2)
            if a + b + c == n:
                return a * b * c


def p9(n):
    for a in range(1, n):
        for b in range(a, n):
            c = sqrt(a ** 2 + b ** 2)
            if a + b + c == n:
                return a * b * c


def p10(n):
    t = 0
    for a in range(5, n, 2):
        if _is_prime(a):
            t += a
    return t
    return sum(a for a in range(5, n, 2) if _is_prime(a)) + 5


def p12(n):
    def tri_num(i):
        return i * (i + 1) // 2

    for a in range(1 << 32):
        if _get_factors(tri_num(a)) > n:
            return a


def p13(n): return str(sum(list(map(int, n))))[:10]


def p14(n):
    def collatz(x):
        t = [x]
        while x != 1:
            x = x // 2 if x % 2 == 0 else 3 * x + 1
            t.append(x)
        return t

    longest = 0, 0
    for a in range(3, n):
        x = collatz(a)
        if len(x) > longest[1]:
            longest = a, len(x)

    return longest


def p15(n): return len(set(permutations(list('rd' * n), n)))


def p16(n, e): return sum(map(int, str(n ** e)))


def p18(x):
    x = [list(map(int, a.split(' '))) for a in x.split('\n')[::-1]]
    for r, row in enumerate(x[:-1]):
        for c, e in enumerate(row[:-1]):
            n = row[c + 1]
            m = max((n, e))
            x[r + 1][c] = m + x[r + 1][c]
    return x[-1][0]


def p67(x):
    return p18(x)


def p20(x):
    return sum(map(int, str(factorial(x))))


def p25(n):
    for i in range(1, 1 << 32):
        if len(str(_fib(i))) >= n:
            return i


if __name__ == '__main__':
    print(p25(1000))
