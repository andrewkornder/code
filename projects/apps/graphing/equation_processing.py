operations = {
    '-': lambda a, b: a - b,
    '+': lambda a, b: a + b,
    '*': lambda a, b: a * b,
    '/': lambda a, b: a / b
}


def solve(equation, x):
    total = 0
    op = operations['+']
    for term in equation.split():
        if not term:
            continue
        if term in '-+*/':
            op = operations[term]
            continue

        if '/' in term:
            s = term.index('/')
            total = op(total, term)
            continue

        if '^' in term:
            base, e = term.split('^')
            e = replace_x(e, x)
            if 'x' in base:
                term = replace_x(base, x ** e)
            else:
                term = float(base) ** e

        else:
            term = replace_x(term, x)

        total = op(total, term)
    return total


def replace_x(term, x):
    """just turns a term into a number (removing coefficients and x-values)"""
    if 'x' not in term:
        return float(term)
    if term == '-x':
        return -x
    if term == 'x':
        return x
    coef = term[:term.index('x')]
    return float(coef) * x
