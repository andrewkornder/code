import PyDictionary as pd

dictionary = pd.PyDictionary()
while True:
    word = input('word: ')
    meaning = dictionary.meaning(word)
    print("\n\nAS DICTIONARY DATA STRUCTURE:\n", meaning)
    print("\nLooping through to get definitions:\n")
    for part_of_speech, meanings_list in meaning.items():
        print("PART OF SPEECH: ", part_of_speech)
        print("Definitions:")
        for i, m in enumerate(meanings_list):
            print(str(i + 1)+'.', m, '\n\n')
    print('====='*10) 
