import os
from pprint import pprint


def get_py(folder, total=None, venv=False):
    if total is None:
        total = []

    files = list(os.walk(folder))
    for f in files:
        total += [os.path.join(f[0], file) for file in f[2] if file[-3:] == '.py']

    if not venv:
        return total
    return [f for f in total if 'venv' not in f]


all_py = get_py('../', venv=False)
numbers = {}
for py in all_py:
    try:
        with open(py) as f:
            docstring = False
            lines = f.readlines()
            code = 0
            cmts = 0
            dc = 0
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

    name = py.split('\\')[-1]
    numbers[name] = (len(lines), code, cmts, dc)

sums = [0, 0, 0, 0]
for val in numbers.values():
    for i, v in enumerate(val):
        sums[i] += v

pprint(sorted(numbers.items(), key=lambda x: x[1][1]))
print(sums)
