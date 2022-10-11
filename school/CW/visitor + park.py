#visitor.py

from random import randint, choice

class Visitor:
    def __init__(self, name=None, x=0, y=0, energy=100):
        self.x_loc, self.y_loc, self.energy = x, y, energy
        
        self.happiness = randint(0, 100)
        if name is None:
            f = choice([a for a in open('ALLFirstNames.txt').read().split() if len(a) < 8])
            self.name = f + ' ' + choice([a for a in open('Lastnames.txt').read().split() if len(a) < 8])
        else: self.name = name
    
    def move(self):
        m = choice(list(zip([0, 0, 1, -1], [1, -1, 0, 0])))
        self.x_loc += m[0]
        self.y_loc += m[1]
        
        self.energy -= 2
        self.happiness += 3


all_vis = [Visitor(x=10, y=17) for _ in range(100)]
for v in all_vis:
    for _ in range(5):
        v.move()
    print(f'moved: {v.name} to {v.x_loc}, {v.y_loc}\n\t{v.name} is \
          now at {v.happiness} happiness and {v.energy} energy')
print('\n\n')
for i in range(10):
    v = choice(all_vis)
    print(f'\t{v.name}\t  {v.happiness} happiness')