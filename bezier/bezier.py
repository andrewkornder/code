from bezier_graph import BezierGraph
from functools import reduce


def bezier_fast(points, t):
    n, t0 = len(points) - 1, 1 - t
    coef, final = t0 ** n, []
    for k, point in enumerate(points):
        final.append(point * coef)
        coef *= t * (n - k) / (k + 1) / t0
    return reduce(lambda a, b: a + b, final)


def bezier_recursive(vectors, t):
    return (lambda l: l[0] if len(l) == 1 else bezier_recursive(l, t))(
        [vectors[i].draw_lerp(p, t) for i, p in enumerate(vectors[1:])]
        )


def bezier(vectors, t, illus, type=1):
    if not type and illus and len(vectors) == 2:
        (lambda a, b: a.canvas.create_line(*a.coords, *b.coords, fill='white', tags=('child',), width=a.radius / 5))\
            (*vectors)
    return (bezier_fast if type else bezier_recursive)(vectors, t)


if __name__ == '__main__':
    _g = BezierGraph(1000, 1000, bezier)
    _g.run()

    k = 5
    n = 1
    for i in range(k):
        for c in ((0, 0), (1000, 0), (1000, 1000), (0, 1000))[:4 if k - i - 1 else n]:
            _g.add_point(*c)

    _g.run()
