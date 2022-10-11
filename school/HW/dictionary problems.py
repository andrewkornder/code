def display_inventory(loot):
    print('Inventory:')
    total = 0
    for k, v in loot.items():
        if v>1:
            print('\t', v, '\t', str(k)+'s')
        else:
            print('\t', v, '\t', k)            
        total+=v
    print('Total number of items:', total)

def add_to_inventory(loot, dragon_loot):
    for item in dragon_loot:
        if item in loot:
            loot[item] += 1
            continue
        loot[item] = 1
    return loot

def scrabble_score(word):
    letter_scores = {'a': 1,
                     'e': 1, 
                     'i': 1, 
                     'l': 1, 
                     'o': 1, 
                     'n': 1, 
                     's': 1, 
                     'r': 1, 
                     'u': 1, 
                     't': 1, 
                     'd': 2, 
                     'g': 2, 
                     'b': 3, 
                     'c': 3,
                     'm': 3, 
                     'p': 3, 
                     'f': 4, 
                     'h': 4, 
                     'w': 4, 
                     'v': 4, 
                     'y': 4, 
                     'k': 5, 
                     'j': 8, 
                     'x': 8, 
                     'q': 10, 
                     'z': 10}
    return sum([letter_scores[letter] for letter in word])
def get_average(grades):
    weights = [0.1, 0.3, 0.6]
    w_avg = 0
    for pos, grade_type in enumerate(list(grades.keys())[1:]):
        curr = 0
        curr_grades = grades[grade_type]
        for score in curr_grades:
            curr += score
        
        curr = curr/len(curr_grades) * weights[pos]
        
        w_avg += curr
    return round(w_avg, 2)

def letter_grade(score):
    letters = {10:'F',
               20:'F',
               30:'F',
               40:'F',
               50:'F',
               60:'D',
               70:'C',
               80:'B',
               90:'A'}
    score = score - (score % 10)
    return letters[score]

def get_class_average(classavg):
    total = 0
    for avg in classavg:
        total += avg
    return total/len(classavg)


loot = {'rope':1, 'torch':6, 'gold coin':42, 'dagger':1, 'arrow':12}
dragon_loot = ['gold coin', 'dagger', 'gold coin', 'gold coin', 'ruby']
print('=====INVENTORY PROBLEMS=====\n')
loot = add_to_inventory(loot, dragon_loot)
#print('\t'+', '.join(map(str, loot)))
display_inventory(loot)


print('\n=====SCRABBLE PROBLEMS=====\n')
word = 'cat'
print('\''+word+'\' scores for', scrabble_score(word))


print('\n=====GRADEBOOK PROBLEMS=====\n')
gradebook = {
    'lloyd':{
        "name": "Lloyd",
        "homework": [90.0, 97.0, 75.0,92.0],
        "quizzes" : [88.0, 40.0, 94.0],
        "tests" : [75.0, 90.0]
    },
    'alice':{
        "name" : "Alice",
        "homework" : [100.0, 92.0, 98.0, 100.0],
        "quizzes" : [82.0, 83.0, 91.0],
        "tests" : [89.0, 97.0]
    },
    'tyler':{
        "name": "Tyler",
        "homework" : [0.0, 87.0, 75.0, 22.0],
        "quizzes" : [0.0, 75.0, 78.0],
        "tests" : [100.0, 100.0]
    }
}

classavg = []
for grade in gradebook:
    w_avg = get_average(gradebook[grade])
    classavg.append(w_avg)
    letter = letter_grade(w_avg)
    print(gradebook[grade]['name']+':')
    print('\t'+str(w_avg), '/', letter)
classavg = round(get_class_average(classavg), 2)
print('class avg:', classavg)
    