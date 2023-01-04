import os
from pprint import pprint


def get_py(folder, total=None, venv=False):
    if total is None:
        total = []

    files = list(os.walk(folder))
    for f in files:
        total += [os.path.join(f[0], file) for file in f[2] if file[-3:] == '.py']

    return total


def get_nums(folder, ignored=()):
    all_py = get_py(folder, venv=False)
    numbers = {}
    for py in all_py:
        try:
            with open(py) as f:
                docstring = False
                lines = f.readlines()
                code = cmts = dc = 0
                for line in lines:
                    if not line.strip():
                        continue
                    code += 1
                    if '#' in line or docstring:
                        cmts += 1
                    elif '"""' in line or "'''" in line:
                        dc += 1
                        if not ('"""' in line[4:] or "'''" in line[4:]):
                            docstring = not docstring
        except Exception:
            continue

        parts = py.split('\\')
        if any(f in parts[0] for f in ignored):
            continue
        numbers[f'{parts[0]}/.../{parts[-1]}'] = (len(lines) + 1, code, cmts, dc)

    sums = [0, 0, 0, 0]
    for val in numbers.values():
        for i, v in enumerate(val[1:]):
            sums[i] += v

    print((f'total lines of code: {sums[0]}\nlines of code (omitting \\n\'s ' +
           f'and comments/docstrings): {sums[1]}\ntotal comments: {sums[2]}\ntotal docstrings: {sums[3]}'))

    return sorted(numbers.items(), key=lambda x: x[1][1])


pprint(get_nums(input(), ignored=('venv', 'py311', )))
