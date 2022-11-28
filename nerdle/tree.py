from itertools import product
from tkinter import Canvas, Tk, Label


CHARS = '1234567890-+*/='
BLACK = 0
YELLOW = 1
GREEN = 2


class Nerdle:
    @staticmethod
    def score(guess, answer):
        r, answer = [0] * len(guess), list(answer)

        for i, (gl, al) in enumerate(zip(guess, answer)):
            if gl == al:
                r[i] = 2
                answer[i] = ''

        for i, l in enumerate(guess):
            if not answer[i]:
                continue

            if l in answer:
                r[i] = 1
                answer[answer.index(l)] = ''
            else:
                r[i] = 0
        return r

    @staticmethod
    def _test_equation(equation):
        rhs, lhs = equation.split('=')
        if any(a * 2 in equation for a in '+-/=*'):
            return False
        if any('/0' in x or not x or x in '-+=*/' for x in (rhs, lhs)):
            return False
        try:
            exec(f'1 / (({lhs}) - ({rhs}))')
        except ZeroDivisionError:
            return True
        except SyntaxError:
            return False
        return False

    @staticmethod
    def _get_permutations(length, validate=lambda *args: args):
        """
        a valid equation will always have the lhs and right hand side equal, so lhs - rhs will be 0
        we can exploit this to get an error when running exec(" 1 / (lhs - rhs) "),
        this way we dont have to code a parser for math eq

        a valid solution will have all operations on the lhs, so we remove those to filter for solutions only
        """

        eq = product('1234567890-+*/=', repeat=length)
        for string in eq:
            string = ''.join(string)
            spl = string.split('=')
            if len(spl) != 2 or not Nerdle._test_equation(string) or any(x in spl[1] for x in '-+/*'):
                continue
            if validate(string):
                yield string

        return None

    def __init__(self, length, validate=lambda *args: args):
        self.permutations = self._get_permutations(length, validate)

    def validate(self, string):
        return self._test_equation(string)


class TreeDisplay:
    def __init__(self, tree, polygamous=False):
        self.tree = tree
        self.nodes = tree.nodes

        tw, th = len(self.nodes[-1]), len(self.nodes)
        self.ly = 200
        self.w, self.h = 1800, 700
        self.s, self.ly = max(3.0, (self.w - 20) / (4 * tw)), self.h / (th + 0.5)
        self.outline = '' if self.s == 3.0 else 'black'

        self.root = Tk()
        self.root.geometry(f'{self.w}x{self.h + 50}')

        self.canvas = Canvas(self.root, width=self.w, height=self.h)
        self.canvas.pack()

        self.label = Label(self.root, text='')
        self.label.pack()

        def ge(tags):
            string, p = '', (lambda i, j: self.nodes[j][i])(*map(int, tags[1].split(',')))
            while p.parent is not None:
                string += p.value
                p = p.parent
            return string[::-1]

        self.canvas.tag_bind('node', "<Enter>", lambda _: self.label.config(
            text=self.canvas.gettags(self.canvas.find_withtag('current')[0])[0]))
        self.canvas.tag_bind('all', "<Leave>", lambda _: self.label.config(text=''))
        if not polygamous:
            self.canvas.tag_bind('line', "<Enter>", lambda _: self.label.config(
                text=ge(self.canvas.gettags(self.canvas.find_withtag('current')[0]))))

        list(map(self.create_layer, range(len(self.nodes))))
        self.canvas.tag_raise('line')
        self.root.mainloop()

    def create_layer(self, i):
        def par(x, p, lcolor, j):
            nj = self.nodes[i - 1]
            self.canvas.create_line(x, y, (self.w - 20) / len(nj) * (nj.index(p) + 0.5) + 10, y - self.ly,
                                    fill=lcolor, width=0.1, tags=('line', f'{j},{i}'))

        layer = self.nodes[i]
        sw, y = (self.w - 20) / len(self.nodes[i]), self.ly * (i + 1)
        for j, node in enumerate(layer):
            color, lcolor = ('#888888', '#bbbbbb') if node.active else ('#c81111', '#a60000')

            x = 10 + (j + 0.5) * sw
            self.canvas.create_oval(x - self.s, y - self.s, x + self.s, y + self.s,
                                    fill=color, tags=(node.value, 'node'), outline=self.outline)
            if node.parent is not None:
                if isinstance(node.parent, Node):
                    par(x, node.parent, lcolor, j)
                else:
                    [par(x, p, lcolor, j) for p in node.parents]


class Node:
    @classmethod
    def parent(cls):
        return Node(None, None)

    def __init__(self, parent, value):
        self.parent = parent
        self._children = []
        self.value = value
        self.active = True

        if parent is not None and isinstance(parent, Node):
            self.parent.add(self)

    def add(self, node):
        self._children.append(node)

    @property
    def children(self): return [child for child in self._children if child.active]

    @property
    def branch_size(self):
        if self.children:
            return sum(1 + node.branch_size for node in self.children)
        return 0

    def delete(self):
        self.active = False
        [node.delete() for node in self._children]

    def __repr__(self):
        return f'Node({self.parent.value}) -> Node({self.value})' if self.parent is not None else\
            f'None -> Node({self.value})'

    def __getitem__(self, item):
        for node in self.children:
            if node.value == item:
                return node
        raise ValueError(f'{item} was not found in self.children')

    def __contains__(self, item):
        return any(node.value == item for node in self.children)


class PolygamousChildNode(Node):
    def __init__(self, parents, value):
        super().__init__(parents, value)
        self.parents = self.parent
        del self.parent

    def create_marriage(self, parent):
        self.parents.append(parent)

    def delete(self):
        self.active = False

    def __repr__(self):
        return f'Node({[p.value for p in self.parents]}) -> Node({self.value})' if self.parents != [None] else \
            f'None -> Node({self.value})'


class PolygamousTree:
    @classmethod
    def from_list(cls, entries, **kwargs):
        parent, entries = Node.parent(), list(entries)

        length = len(entries[0])
        assert {length} == set(map(len, entries))

        nodes = [[parent]]
        for entry in entries:
            p = parent
            for i, char in enumerate(entry):
                if char in p:
                    p = p[char]
                    continue
                p = Node(p, char)

        return cls(parent, nodes, **kwargs)

    @classmethod
    def from_charset(cls, length, /, chars=CHARS, **kwargs):
        parent = PolygamousChildNode.parent()
        nodes = [[parent]]

        for depth in range(length):
            nodes.append([PolygamousChildNode(nodes[depth], c) for c in chars])

        return cls(parent, nodes, **kwargs)

    def __init__(self, parent, nodes, guess, info, clean=True):
        self.nodes, self.parent = nodes, parent

        if clean:
            self.clean_up(guess, info)

    def display(self):
        TreeDisplay(self, True)
        return self

    def clean_up(self, guess, info):
        for i, (g, a) in enumerate(zip(guess, info)):
            if a == BLACK:
                for layer in self.nodes:
                    for node in layer:
                        if node.value == g:
                            node.delete()
            elif i + 1 < len(self.nodes) and a == GREEN:
                for node in self.nodes[i + 1]:
                    if node.value != g:
                        node.delete()


class MonogamousTree:
    @classmethod
    def from_list(cls, entries, **kwargs):
        parent, entries = Node.parent(), list(entries)
        nodes = [[parent]]
        for entry in entries:
            p = parent
            for i, char in enumerate(entry):
                if char in p:
                    p = p[char]
                else:
                    p = Node(p, char)
                    if i + 1 >= len(nodes):
                        nodes.append([p])
                    else:
                        nodes[i + 1].append(p)

        return cls(parent, nodes, **kwargs)

    @classmethod
    def from_charset(cls, length, /, chars=CHARS, **kwargs):
        parent = Node.parent()

        nodes = [[parent]]
        for depth in range(length):
            nodes.append([Node(p, char) for p in nodes[-1] for char in chars])

        return cls(parent, nodes, **kwargs)

    def __init__(self, parent, nodes, guess, info, clean=True):
        self.parent, self.nodes = parent, nodes

        before = parent.branch_size

        if clean:
            self.clean_up(guess, info)
            print(f'{self.parent.branch_size:e}')

        self._ratio = parent.branch_size / before if clean else 1

    def clean_up(self, guess, info):  # median ratio is 0.351 (not great tbh)
        for i, (g, a) in enumerate(zip(guess, info)):
            if a == BLACK:
                for layer in self.nodes:
                    for node in layer:
                        if node.active and node.value == g:
                            node.delete()
                continue

            if i + 1 >= len(self.nodes):
                continue

            for node in self.nodes[i + 1]:
                if node.active and (node.value == g) == (a == YELLOW):
                    node.delete()

    def display(self):
        TreeDisplay(self)
        return self

    def generate_remaining(self, length):
        return Nerdle(length, validate=lambda string: string[:len(self.nodes) - 1] in self.get_options())

    def get_options(self):
        def g(node, part=''):
            if node.children:
                return [g(child, part + node.value) for child in node.children]
            return part + node.value

        return sum([g(child) for child in self.parent.children], [])

    @property
    def ratio(self):
        return self._ratio


if __name__ == '__main__':
    _test = {
        'guess': '2*3-1=+5',
        'info': [1, 2, 0, 0, 1, 2, 0, 1],
        'clean': True,
    }

    assert len(_test['info']) == len(_test['guess'])

    _g = Nerdle(5)
    MonogamousTree.from_list(_g.permutations, **_test).display()

    PolygamousTree.from_charset(5, **_test).display()
