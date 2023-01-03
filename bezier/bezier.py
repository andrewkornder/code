from bezier_graph import BezierGraph
from functools import reduce


def bezier_fast(points, t):
    n, t0 = len(points), 1 - t
    coef, final = t0 ** (n - 1), []
    for k, point in enumerate(points):
        final.append(point * coef)
        coef *= t / t0 * (n / (k + 1) - 1)
    return reduce(lambda a, b: a + b, final)


def bezier_recursive(vectors, t):
    return (lambda l: l[0] if len(l) == 1 else bezier_recursive(l, t))(
        [vectors[i].draw_lerp(p, t) for i, p in enumerate(vectors[1:])])
    
    
def bezier_full(vectors, t, illus, type=1):
    """type: 0 for recursive
             1 for iterative"""
    if not type and illus and len(vectors) == 2:
        (lambda a, b: a.canvas.create_line(*a.coords, *b.coords, fill='white', tags=('child',), width=a.radius / 5))\
            (*vectors)
    return (bezier_fast if type else bezier_recursive)(vectors, t)


import numpy as np


def bspline(self, degree=3, periodic=False):
    cv = np.asarray(self.points)

    if periodic:
        cv = (lambda factor, fraction: np.concatenate((cv,) * factor + (cv[:fraction],)))(*divmod(self.length + degree + 1, self.length))

    count = len(cv)
    degree = np.clip(degree, 1, degree if periodic else count - 1)
    kv = np.arange(0 - degree, count + degree + degree - 1, dtype='int') if periodic else kv = np.concatenate(([0] * degree, np.arange(count - degree + 1), [count - degree] * degree))

    return np.array(si.splev(np.linspace(periodic, (count - degree), self.N), (kv, cv.T, degree))).T


if __name__ == '__main__':
    _g = BezierGraph(1000, 1000, bezier_full)

    _k = 5
    _n = 1
    for _i in range(_k):
        for c in ((0, 0), (1000, 0), (1000, 1000), (0, 1000))[:4 if _k - _i - 1 else _n]:
            _g.add_point(*c)

    _g.run()
