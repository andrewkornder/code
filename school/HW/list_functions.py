def rotate_amt(shift, nums):
    return nums[-shift:]+nums[:shift]



def is_paired_with_square(nums):
    pairs = [(nums[i], nums[i+1]) for i in range(len(nums)-1) if i%2 == 0]
    ans = [pair[0]**2 == pair[1] or pair[1]**2 == pair[0] for pair in pairs]
    return any(ans)



def number_of_evens(nums):
    return len(['' for i in nums if i % 2 == 0])
    
def longest_increasing(nums):
    pairs, current, largest = [(nums[i], nums[i+1]) for i in range(len(nums)-1)], [], []
    for pair in pairs:
        if len(current)>len(largest):
            largest = current        
        if pair[0]<pair[1]:
            current.append(pair[0])
            current.append(pair[1])
        else:
            current = []
    largest[1:-1] = largest[1:-1:2]
    
    return largest

def splittable(nums):
    rval = []
    if sum(nums) % 2 == 0:
        goal = sum(nums)/2
    else:
        return None
    for i in range(len(nums)):
        if sum(nums[:i]) == sum(nums[i:]):
            return nums[:i], nums[i:]
    return None

def tournament_winner(s1, b1, s2, b2):
    t1 = [score * bonus for score in s1 for bonus in b1]
    t2 = [score * bonus for score in s2 for bonus in b2]
    if sum(t1)>sum(t2):
        return 'team 1 won'
    return 'team 2 won'
def num_of_clumps(nums):
    last_clump = None
    counter = 0
    pairs = [(nums[i], nums[i+1]) for i in range(len(nums)-1)]
    for pair in pairs:
        if pair[0] == pair[1]:
            if pair[0] == last_clump:
                continue
            last_clump = pair[0]
            counter+=1
    
    return counter

def benefit_from_round(grades, names):
    benefits = [round(grade)>grade for grade in grades]
    
    print(benefits)
    return benefits[:len(names)]

def my_fn():
    
    return None

letterFrequency = {'E' : 12.0,
                   'T' : 9.10,
                   'A' : 8.12,
                   'O' : 7.68,
                   'I' : 7.31,
                   'N' : 6.95,
                   'S' : 6.28,
                   'R' : 6.02,
                   'H' : 5.92,
                   'D' : 4.32,
                   'L' : 3.98,
                   'U' : 2.88,
                   'C' : 2.71,
                   'M' : 2.61,
                   'F' : 2.30,
                   'Y' : 2.11,
                   'W' : 2.09,
                   'G' : 2.03,
                   'P' : 1.82,
                   'B' : 1.49,
                   'V' : 1.11,
                   'K' : 0.69,
                   'X' : 0.17,
                   'Q' : 0.11,
                   'J' : 0.10,
                   'Z' : 0.07 }



