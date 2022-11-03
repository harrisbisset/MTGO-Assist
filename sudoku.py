from random import seed
from random import randint

letters = ['a', 'b', 'c']
dict = {(letters[int(number / 3)] + str(number % 3)):{(letters[int(number / 3)] + str(number % 3)):'' for number in range(0,9)} for number in range(0,9)}
#dict = {'a0':{'a0:':'', 'a1':'', etc.}, 'a1':{etc.}, etc.}

seed(1)

#goes through each number
for number in range(0,9):

    #goes through each 9*9 grid
    for i in dict:

        #gets a random square in the grid
        num = randint(0, 8) % 3

        #gets the row of the grid
        letter = letters[num]

        #a2
        total = letter + str(num)
        

        #check box
        for rowcol in range(0,9):
            if dict[i][(letters[int(rowcol / 3)] + str(rowcol % 3))] == dict[i][total] and total != rowcol:
                pass 

        #check column
        for cols in [letters[int(grid / 3)] + str(grid % 3) for grid in range(0,9)]:
            #print(cols)
            for col in range(0,2):
                if dict[i][total] == dict[cols][letters[col]+str(col)] and total != cols:
                    pass
        
        #check row
        for rows in [letter + str(grid % 3) for grid in range(0,9)]:
            for row in range(0,2):
                if dict[i][total] == dict[letters[row]+str(row)][rows] and (total != rows or i != letters[row]+str(row)):
                    pass


