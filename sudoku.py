import random
letters = ['a', 'b', 'c']
#dict = {letters[number-1 % 3] + str(number):{letters[num1-1 % 3] + str(num1):'' for num1 in range(1,5)} for number in range(1,5)}
#print(dict)

if (number / 3) > 1:

dict = {letters[int(number/3)] for number in range(1,10)}


dict = {'a1':{'a1:':'', 'a2':''}, 'a2':''}


for b in range(1,9):
    for i in dict:
        num = getRandNum(1,9)
        letter = 'a'
        while num > 3:
            num = num - 3
            letter = chr(ord(letter)+1)

        for x in dict:
            if x[0] == i[0] or x[1] == i[1]:
                for n in x:
                    if (n[0] == i[0] or n[1] == i[1]) and n != b:
                        dict[i][str(num) + letter] = b
