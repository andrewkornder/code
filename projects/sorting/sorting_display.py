import tkinter
import random
import time
from timeit import default_timer as timer
import itertools
import os

global root, canvas, scales, limit_entry
global curr_op, operations, start_button
global delay_var, to_cancel, repeats
global dimX, dimY, canvas_dimY, speed


def insertion_sort(unsorted_list, dis=True):
    comps = 0
    for i, e in enumerate(unsorted_list):
        for idx, element in enumerate(unsorted_list[:i]):
            comps += 1
            if element > e:
                del unsorted_list[i]
                unsorted_list.insert(idx, e)
                break
        if to_cancel:
            return None
        if dis:
            display(unsorted_list, search=False)

    return unsorted_list, len(unsorted_list), comps


def counting_sort(unsorted_list, dis=True):
    fl = []
    nl = {i: [] for i in range(min(unsorted_list), max(unsorted_list) + 1)}
    for a in unsorted_list:
        nl[a].append(a)

        fl = []
        for b in nl.values():
            fl += b
        if dis:
            display(fl)
        if to_cancel:
            return None

    return fl, 2, 0


def radix_lsd_sort(unsorted_list, dis=True):
    length = len(str(max(unsorted_list)))

    for digit in range(length):
        buckets = {i: [] for i in range(10)}

        for item in unsorted_list:
            buckets[item // 10 ** digit % 10].append(item)

        unsorted_list = list(itertools.chain.from_iterable(buckets.values()))
        if dis:
            display(unsorted_list)

    return unsorted_list, length, 0


def bucket_sort(unordered_list, dis=True):
    power = 10 ** len(str(max(unordered_list)))
    floatlist = [ele / power for ele in unordered_list]
    buckets = {a: [] for a in range(10)}
    unsorted_list = []
    it = 0
    comps = 0
    for ele in floatlist:
        n = int(ele * 10)
        buckets[n].append(ele)

    for b in buckets.values():
        if not len(b):
            continue
        b = [int(a * power) for a in b]
        b, i, c = insertion_sort(b, dis=True)
        unsorted_list += b
        it += i / 10
        comps += c
        if to_cancel:
            return None
        if dis:
            display(unsorted_list + unordered_list[len(unsorted_list):])

    return unsorted_list, int(it + 10), comps


def bubble_sort(unordered_list, dis=True):
    c = True
    it = 0
    comps = 0
    m = len(unordered_list) - 1
    while c:
        c = False
        comps += m * 2 - 1

        for i, e in enumerate(unordered_list):
            if i == m:
                break
            ni = i + 1
            n = unordered_list[ni]
            if e > n:
                c = True
                unordered_list[ni] = e
                unordered_list[i] = n

        if to_cancel:
            return None
        if dis:
            display(unordered_list, search=False)
        it += 1

    return unordered_list, it, comps


def solar_bit_flip_sort(unsorted_list, dis=True):
    while any([a > unsorted_list[i + 1] for i, a in enumerate(unsorted_list[:-1])]):
        if to_cancel:
            return None
        if dis:
            display(unsorted_list)

    return unsorted_list, 0, 0


def stalin_sort(unsorted_list, dis=True):
    comps = 0
    ln = len(unsorted_list) + 1
    for i, a in enumerate(unsorted_list):
        comps += ln - i
        for e in unsorted_list[i + 1:]:
            if e < a:
                unsorted_list.remove(e)
                if dis:
                    display(unsorted_list)
            if to_cancel:
                return None
    return unsorted_list, 1, comps


def linear_search(unsorted_list):
    if not unsorted_list:
        return None

    target = random.choice(unsorted_list)
    ln = len(unsorted_list)
    for i, a in enumerate(unsorted_list):
        if a == target:
            canvas.delete('all')
            maximum = max(unsorted_list)
            box_width = (dimX - 50) / ln
            x, top = 25 + i * box_width, (canvas_dimY - 70) - (
                    target * (canvas_dimY - 100)) / maximum
            if box_width < 2:
                box_width = 2

            canvas.create_rectangle(x, top, x + box_width, (canvas_dimY - 50),
                                    fill='red', outline='')

            return i, i + 1, i + 1

        if to_cancel:
            return None

        display(unsorted_list, search=True, ss=(i, ln))


def binary_search(unordered_list):
    sorted_list = radix_lsd_sort(unordered_list)[0]
    target = random.choice(sorted_list)

    index, iterations = bs_helper(sorted_list, target, 0, len(sorted_list))

    if index is None:
        return None

    canvas.delete('all')

    maximum = sorted_list[-1]
    box_width = (dimX - 50) / len(sorted_list)
    x, top = 25 + index * box_width, (canvas_dimY - 70) - (
            target * (canvas_dimY - 100)) / maximum
    if box_width < 2:
        box_width = 2

    canvas.create_rectangle(x, top, x + box_width, (canvas_dimY - 50), fill='red', outline='')

    return index, iterations, iterations


def bs_helper(unsorted_list, e, start, stop, c=0):
    display(unsorted_list, search=True, ss=(start, stop))
    i = (start + stop) // 2
    t = unsorted_list[i]
    if to_cancel:
        return None, None
    if t == e:
        return i, c
    if t > e:
        return bs_helper(unsorted_list, e, start, i, c + 1)
    return bs_helper(unsorted_list, e, i + 1, stop, c + 1)


def selection_sort(unordered_list, dis=True):
    length = len(unordered_list)
    nl = []
    comps = 0
    for _ in range(length):
        m = min(unordered_list)
        comps += length
        nl.append(m)
        unordered_list.remove(m)
        if to_cancel:
            return None
        if dis:
            total = nl + unordered_list
            display(total)

    return nl, length, comps


def selection_min_max_sort(unordered_list, dis=True):
    nl = []
    length = len(unordered_list)
    for i in range(int(length / 2)):
        m = max(unordered_list)
        mn = min(unordered_list)
        nl.insert(i, m)
        nl.insert(i, mn)

        unordered_list.remove(m)
        unordered_list.remove(mn)

        if dis:
            display(nl+unordered_list)
        if to_cancel:
            return None

    if len(nl) != length:
        nl.insert(i + 1, unordered_list[0])
        if dis:
            display(nl)

    return nl, length / 2, length ** 2


def bogo_sort(unsorted_list, dis=True):
    it = 0
    comps = 0
    while any(a > unsorted_list[i + 1] for i, a in enumerate(unsorted_list[:-1])):
        it += 1
        random.shuffle(unsorted_list)
        if dis:
            display(unsorted_list)
        if to_cancel:
            return None

    return unsorted_list, it, comps


def display(lo, search=False, ss=None,
            maximum=None):  # ss is (start, stop) so binary_search can be displayed well
    if not len(lo):
        return

    if search:
        start, stop = ss
        unsorted_list = [a if start <= i <= stop else None for i, a in enumerate(lo)]
    else:
        unsorted_list = lo[:]
    canvas.delete('all')
    t_height = canvas_dimY - 70

    if maximum is None:
        maximum = max(lo)

    box_width = (dimX - 50) / len(unsorted_list)

    for i, num in enumerate(unsorted_list):
        c = 'black'

        if num is None:
            continue

        oc = ''
        x, top = 25 + i * box_width, (num * t_height) / maximum
        x1 = x + box_width + 1
        canvas.create_rectangle(x, t_height - top, x1, (canvas_dimY - 50),
                                fill=c, outline=oc)

    if delay_var.get():
        time.sleep(speed.get() / 10)

    canvas.update()


def cancel_sort():
    global to_cancel

    to_cancel = True


def start_op():
    func = operations[curr_op.get()]
    limit = limit_entry.get()
    length = scales[1].get()

    canvas.delete('all')
    canvas.create_text((dimX / 2), 30, text='creating list',
                       font=('Niagara Solid', 20))
    canvas.update()

    if limit.isnumeric() and int(limit) > length:
        list_range = int(limit)
    else:
        list_range = length + 2

    unordered_list = random.sample(range(1, list_range), length)
    print(f'{unordered_list[:5]}...{unordered_list[-5:]}')

    if repeats.get() and len(unordered_list) > 10:
        amt = int(len(unordered_list) / 10)
        unordered_list = unordered_list[:-amt] + random.sample(unordered_list,
                                                               amt)

    display(unordered_list)

    start_button.config(text='stop', command=cancel_sort)

    begin = timer()
    result = func(unordered_list)

    if result is None:
        global to_cancel
        to_cancel = False
        start_button.config(text='start', command=start_op)
        return

    sorted_list, iterations, comparisons = result

    total_time = timer() - begin
    if func not in [binary_search, linear_search]:
        print('solved in {0}s'.format(total_time))
        print(f'{sorted_list[:5]}...{sorted_list[-5:]}')
    else:
        print('solved: idx = {0}\ntime to solve: {1} with {2} guesses'.format(
            sorted_list, total_time, iterations))

    c = 'black' if func != stalin_sort else 'red'

    canvas.create_text((dimX / 2), 40,
                       text='finished sorting\n{0} iterations and {1} comparisons'.format(
                           iterations, comparisons),
                       font=('Niagara Solid', 20), fill=c)
    canvas.create_text((canvas_dimY - 350), 50,
                       text='{0} seconds'.format(round(total_time, 6)),
                       font=('Niagara Solid', 20), fill=c)

    start_button.config(text='start', command=start_op)


def window():
    global root, canvas, scales, limit_entry
    global curr_op, operations, start_button
    global delay_var, to_cancel, repeats
    global dimX, dimY, canvas_dimY

    to_cancel = False
    dimX = 1800 if os.name == 'nt' else 900
    dimY = 700
    canvas_dimY = 500
    root = tkinter.Tk()
    root.geometry('{0}x{1}+0+0'.format(dimX, dimY))
    root.title('')

    canvas = tkinter.Canvas(root, bg='white', width=dimX, height=canvas_dimY)
    canvas.grid(row=0, column=0, columnspan=5)

    delay_var = tkinter.IntVar(root, 0)
    with_delay = tkinter.Checkbutton(root, variable=delay_var,
                                     onvalue=0, offvalue=1,
                                     text='disable delay?')
    with_delay.grid(row=1, column=0)

    limit_entry = tkinter.Entry(root)
    limit_entry.grid(row=1, column=2)

    repeats = tkinter.IntVar(root, 0)
    repeat_check = tkinter.Checkbutton(root, variable=repeats,
                                       onvalue=1, offvalue=0,
                                       text='add repeats?')
    repeat_check.grid(row=2, column=1)

    scales = []
    create_scales()

    operations = {
        'linear search': linear_search,
        'binary search': binary_search,
        'bubble sort': bubble_sort,
        'insertion sort': insertion_sort,
        'selection sort': selection_sort,
        'boosted selection sort': selection_min_max_sort,
        # 'bucket sort':bucket_sort,
        'counting sort': counting_sort,
        'radix (LSD) sort': radix_lsd_sort,
        'bogo sort': bogo_sort,
        'stalin sort': stalin_sort,
        'solar bit flip sort': solar_bit_flip_sort
    }

    curr_op = tkinter.StringVar(root)
    curr_op.set('radix (LSD) sort')

    operation_picker = tkinter.OptionMenu(root, curr_op, *operations)
    operation_picker.grid(row=1, column=1)

    start_button = tkinter.Button(root, text='start', command=start_op)
    start_button.grid(row=4, column=1)

    root.mainloop()


def create_scales():
    global speed
    speed = tkinter.IntVar(root, 0)

    speed_picker = tkinter.Scale(root, from_=1, to=50, variable=speed,
                                 length=200, orient=tkinter.HORIZONTAL)
    length_picker = tkinter.Scale(root, from_=3, to=8000,
                                  length=200, orient=tkinter.HORIZONTAL)
    length_picker.set(10)

    scales.append(speed_picker)
    scales.append(length_picker)

    s_label = tkinter.Label(root, text='delay', width=15)
    l_label = tkinter.Label(root, text='length', width=15)

    s_label.grid(row=2, column=0)
    l_label.grid(row=2, column=2)

    speed_picker.grid(row=3, column=0)
    length_picker.grid(row=3, column=2)


if __name__ == '__main__':
    window()
