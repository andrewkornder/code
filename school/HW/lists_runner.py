import list_functions as LF

def main():
    list_arg1  = [-5, 3, 0, 99, -234, 2348, 5613, 1000, 5, 25, 77, 5, 99]
    list_arg2 = [99, 101, -4, 5, 10001, 50, 71, 99]
    list_arg3 = [6, 5, 2]
    list_arg4 = [5, 7, 1, 99, 101, 500, 3, 4, 5]  
    
    #4 rotate:
    print("\n4")
    print("\n",list_arg2, "rotated by 4 = \n", LF.rotate_amt(4, list_arg2))
    print("SHOULD BE: [10001, 50, 71, 99, 99, 101, -4, 5]")
    
    #5 pair w/square:
    print("\n5:")
    is_paired = LF.is_paired_with_square(list_arg1)
    
    if is_paired:
        print("\n",list_arg1, "has a number next to it's square!")
    elif is_paired != None:  # in case function doesn't return anything
        LF.is_paired_with_square(list_arg1)
        print("\n",list_arg1, "does not have a number next to it's square :(")
    else:
        print("Uh-oh!  Function never returned True or False")
        
    #6 longest increasing
    print("\n6:")
    print("\n","In", list_arg4,
          "the longest string of increasing values is",
          LF.longest_increasing(list_arg4))
    
    #7 splittable
    print("\n7:")
    print("\n", "Should be: [1,  1, 1], [2, 1]:")
    print(LF.splittable([1, 1, 1, 2, 1]))
    print("\n", "Should be: None")
    print(LF.splittable([20, 1, 1, 2, 1]))
    print("\n", "Should be: [10]")
    print(LF.splittable([10, 10]))

    #8 tournament_winner
    print("\n8:")
    score1 = [55, 23, 655]
    score2 = [33, 100, 500]
    bonus_mult1 = [1, 2, 3]
    bonus_mult2 = [3, 2, 1]
    print("\n","Team #", LF.tournament_winner(score1,
                                         bonus_mult1,
                                         score2,
                                         bonus_mult2))
          
    #9 number of clumps
    print("\n9:")
    c = [35, 5, 5, 7, 93, 54, 2, 2, 2, 4, 4, 1, 2, 2]
    print("\n","In", c, "there are", LF.num_of_clumps(c), "clumps of numbers")

    #10 benefit from round
    print("\n10:")
    names = ["Joe", "Mary", "Ichabod", "John", "Abraham"]
    grades = [76.6, 99.0, 82.1, 89.9, 92.8]
    results = LF.benefit_from_round(grades, names)
    for i in range(len(results)):
        if results[i] == True:
            print("\n",names[i], "will benefit from rounding", grades[i])
        elif results[i] != None:
            print("\n",names[i], "will NOT benefit from rounding", grades[i])

    #11 yours
###############
main()
