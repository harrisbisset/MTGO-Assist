import random
from random import randint

def printBoard(dict):
    for grid in range(0,9):
        print(dict[letters[int(grid/3)] + str(grid % 3)])

def randSquare(letters):
    #gets a random square in the grid
    num = randint(0, 8) % 3

    #gets the row of the grid
    letter = letters[num]

    return letter + str(num)


def checkValidity(total, i, dict, number):

    #check column (should be same number)
    for cols in [(let + str(total[1])) for let in letters]:

        for col in range(0,2):
            if number == dict[cols][letters[col]+total[1]] and i != cols:
                return False
        
    
    #check row (rows and row should be same letter)
    for rows in [i[0] + str(grid % 3) for grid in range(0,9)]:
        for row in range(0,2):
            if number == dict[rows][total[0]+str(row)] and i != rows:
                return False
    
    return True


letters = ['a', 'b', 'c']
dict = {(letters[int(number / 3)] + str(number % 3)):{(letters[int(number / 3)] + str(number % 3)):'#' for number in range(0,9)} for number in range(0,9)}
#dict = {'a0':{'a0:':'', 'a1':'', etc.}, 'a1':{etc.}, etc.}


random.seed(81)


#goes through each number
for number in range(0,9):
    print('number: ' + str(number))
    #goes through each 9*9 grid
    for i in dict:
        print('i: ' + str(i))
        while True:
            #ex = a2/b0
            total = randSquare(letters)

            #checks validity of square
            if checkValidity(total, i, dict, number) != False:
                dict[i][total] = number
                break
            else:
                printBoard(dict)


print(dict)
