#!/usr/bin/python
# list_hacker.py

"""defeats hacker"""

__author__ = "Andrew Kornder"
__version__ = "1.0"


def define():
    first, second = [1, 2, 3, 4], [2, 1, 4]
    a, b = [1, 10, 100], [10, 100, 1]
    c, d = [7, 6, 10, 100, 9999, 108, 7], [10, 7, 6, 9999, 7, 100]
    e, f = [2, 3, 4, 5, 6, 7, 8, 9, 45, 36], [9, 8, 7, 6, 5, 4, 3, 2, 36]
    g, h = [95, 52, 10, 7, 16, 58, 26, 46, 2, 93, 34, 34, 7, 75, 40, 86, 48, 10,
            57,
            24, 36, 96, 65, 34, 75, 95, 51, 37, 88, 58, 52, 55, 36, 38, 21, 41,
            48, 80,
            11, 35, 30, 26, 51, 17, 50, 18, 56, 16, 69, 64], [46, 10, 7, 51, 34,
                                                              7, 40,
                                                              86, 50, 48, 18,
                                                              34, 58, 58, 41,
                                                              75, 35, 11, 26,
                                                              16,
                                                              57, 55, 34, 37,
                                                              69, 21, 26, 51,
                                                              10, 95, 80, 93,
                                                              30, 96, 65, 52,
                                                              88, 38, 2, 64,
                                                              36, 17, 75, 16,
                                                              48, 36, 56, 24,
                                                              52]
    i, j = [100, 99, 100, 99, 100, 99, 100], [99, 100, 99, 100, 99, 100]
    k, l = [866, 271, 695, 954, 570, 413, 550, 922, 469, 129, 970, 951, 926,
            785, 612, 478, 734,
            467, 897, 655, 676, 925, 994, 150, 175, 378, 116, 803, 667, 310,
            110, 379, 402, 533,
            154, 690, 984, 278, 285, 432, 353, 189, 137, 477, 900, 992, 512,
            999, 575, 576, 510,
            402, 549, 820, 338, 586, 597, 464, 398, 993, 720, 291, 281, 376,
            182, 399, 133, 134,
            907, 848, 304, 222, 979, 666, 732, 905, 739, 451, 922, 608, 669,
            750, 795, 755, 603,
            776, 129, 202, 837, 311, 389, 579, 366, 234, 677, 210, 180, 261,
            904, 169], [597,
                        137, 281, 820, 175, 734, 922, 667, 278, 451, 353, 732,
                        848, 579, 510, 464, 608,
                        720, 285, 576, 311, 478, 739, 992, 376, 134, 399, 655,
                        129, 550, 261, 467, 904, 169,
                        970, 785, 750, 154, 189, 979, 304, 271, 116, 202, 900,
                        676, 210, 803, 432, 533, 512,
                        234, 477, 776, 795, 994, 378, 150, 469, 669, 586, 379,
                        993, 402, 310, 366, 389, 951,
                        291, 755, 690, 612, 129, 182, 575, 110, 695, 398, 549,
                        999, 133, 666, 338, 907, 603,
                        402, 905, 413, 922, 897, 954, 837, 222, 180, 926, 677,
                        925, 570, 984]
    return [(first, second, ([3], [])), (a, b, ([], [])), (c, d, ([108], [])),
            (e, f, ([45], [])), (g, h, ([95], [])), (i, j, ([100], [])),
            (k, l, ([866], []))]


def stolen_ID(a0, b0, for_check=False):
    # clone the lists to avoid removing values from passed in lists
    missing = a0[:]
    added = b0[:]

    # removing all the values in both lists, leaving only added values in list B and removed values in list A
    for val in b0:
        if val in missing:
            missing.remove(val)
            added.remove(val)
            # return missing and added values as tuple
    if for_check:
        return missing, added
    # return as string if not used for check()
    return 'missing values: ' + ', '.join(
        map(str, missing)) + '\nadded values: ' + ', '.join(map(str, added))


def check():
    # get the inputs and answers for each check
    tests = define()
    # empty variables for output
    correct = 0
    answers = []
    for test in tests:
        # get answer for current test case
        current = test
        returned = stolen_ID(current[0], current[1], True)

        # checking if returned answer is right or wrong
        if returned == current[2]:
            correct += 1
            answers.append('correct')

        else:
            answers.append('incorrect, returned ' + str(returned)[
                                                    1:-1] + '. correct answer was ' + str(
                current[2])[1:-1])

    # printing all the outputs
    for i in range(len(answers)):
        print('test ' + str(i + 1) + ': ' + answers[i], end='\n')
    print(str(correct) + " correct out of " + str(len(answers)))

    response = input('\n\nsee all answers? (Y/N)\n')

    if response.lower()[0] == 'y':
        for i in range(len(tests)):
            print('\ntest ' + str(i + 1) + ' = ' + str(tests[i][2])[1:-1])


check()
