import random
        
def tests():
    list1 = [x for x in range(500, 1001) if x % 5 == 0 and x%3 != 0]
    list2 = [x ** 3 for x in range(1, 101)]
    list3 = [x for x in list2 if x % 5 == 0 and x % 3 != 0]
    list4 = [random.randint(9000, 99000) for i in range(100)]
    text = 'sample text'
    list5 = [w for w in text.split() if len(w) > 4 and len(w) < 8]
    list6 = [[('b', 'r')[x % 2] for x in range(8)]] * 8
    
    return list1, list2, list3, list4, text, list5, list6,
        
def checkerboard():
    
    # list7a = 
    list6 = [[('b', 'r')[x % 2] for x in range(8)]] * 8
    list7 = [(list6[i][1:] + list6[i][:1], list6[i])[i % 2] for i in range(len(list6))]
    
    return list7
list1 = checkerboard()
for o in list1:
    print(o)
