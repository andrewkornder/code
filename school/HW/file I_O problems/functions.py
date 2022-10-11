from file_open import get_file
import random, os

def get_words(filename):
    with open(filename, 'r') as f:
        return f.read().replace('\n', ' ').split()
    
def reverse_file(filename):
    with open(filename[:-4] + '_reverse.txt', 'w') as rev:
        with open(filename, 'r') as f:
            lines = f.read().split('\n')
        
        for line in lines:
            line = line.split()
            for word in line:
                rword = word[::-1]
                print(rword)
                rev.write(rword + ' ')
            rev.write('\n')

def file_sum(filename):
    total = 0
    with open(filename, 'r') as f:
        text = f.read()
        words = [w.replace(',', '') for w in text.replace('\n', ' ').split()]
        for word in words:
            if word.replace('.', '').isdigit():
                total += float(word)
        with open(filename[:-4]+'_sum'+'.txt', 'w') as s:
            s.write('SUM = '+str(total)+'\n\n')
            s.write(''.join([a for a in text if a not in '1234567890']))
    print('sum = {0}'.format(total))
    
def contains_word(filename, word='word'):
    with open(filename[:-4]+'_containing_'+word.upper()+'.txt', 'w') as c:
        with open(filename, 'r') as f:
            text = f.read()
        lines, start = [], 0
        for i, char in enumerate(text):
            if char in ['.', '!', '?']:
                lines.append(text[start:i + 1])
                start = i + 1
        for line in lines:
            if ' '+word+' ' in line:
                c.write(line.replace(word, word.upper()) + '\n')

def anagram(filename):
    with open(filename, 'r') as f:
        lines = f.read().split('\n')
    words = []
    for line in lines:
        for punc in list('.,/\'\":;-=+)(*&^%$#@!~`'):
            line = line.replace(punc, '')
        words += line.split()
    target = random.choice(words)
    scramble = ''.join(sorted(target))
    guesses = 10
    print('guess the scrambled word: {0}'.format(scramble))
    while input('guess: ').lower().replace(' ', '') != target:
        guesses -= 1
        print('wrong: {0} guesses left'.format(guesses))
    print('thats right! it took you {0} {1} to get it right'.format(11 - guesses, 'try' if guesses == 10 else 'tries'))

def assemble_an_automatic_alliterative_aria(folder='Assemble An Automatic Alliterative Aria'):
    files = [folder + '/' + file for file in next(os.walk(folder))[2]]
    noun = random.choice(get_words(files[0])).lower()
    start = noun[0]
    sentence = noun.capitalize()+'\'s'
    
    for file in files[:0:-1]:
        sentence += ' '+random.choice([a for a in get_words(file) if a[0] == noun[0]]).lower()
    return sentence
        
def start_op():
    print('pick a function:')
    funcs = {k + 1:v for k, v in enumerate([reverse_file, file_sum, contains_word, anagram, assemble_an_automatic_alliterative_aria])}
    for k, v in funcs.items():
        print('{0} - {1}'.format(k, v.__name__))
    func = funcs[int(input('\n'))]
    if func != assemble_an_automatic_alliterative_aria:
        file = get_file(directory='word_files')
    else:
        file = 'Assemble An Automatic Alliterative Aria'
    if file == '':
        print('no file selected')
        return None
    
    if func == contains_word:
        arg1 = input('which word would you like to search for? ')
        result = func(file, arg1)
    else:
        result = func(file)
    print('\n\n' + 'done' if result is None else result)

if __name__ == '__main__':
    start_op()