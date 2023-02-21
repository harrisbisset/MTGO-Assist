import sqlite3
import sys
import json

#gets data from database to be displayed on table
def openData():
    userConnection = sqlite3.connect("./database/mtgoAssist.db")
    cursor = userConnection.cursor()
    try:
        matches = cursor.execute("SELECT * FROM matches ORDER BY matchID DESC limit 20;").fetchall()
        
        results = {}

        for matchTuple in matches:
            results[matchTuple[0]] = [{}]
            for data in matchTuple:
                if isinstance(data, int) == False:
                    data = json.loads(data)
                    results[matchTuple[0]][0][list(data.keys())[0]] = data[list(data.keys())[0]]

        print(json.dumps(results))
    except:
        pass
    finally:
        cursor.close()
        userConnection.close()




#gets user averages
def getUserData():

    try:
        with open('python\playerName.txt', 'rb') as f:
            player = f.read().decode(encoding='utf-8', errors='replace')
    except:
        print('NA')
        return

    userConnection = sqlite3.connect("./database/mtgoAssist.db")
    cursor = userConnection.cursor()

    matches = cursor.execute("SELECT winner FROM matches;").fetchall()

    results = {}
    for num, match in enumerate(matches):
        results[num] = json.loads(match[0])
    
    winList = []
    count = 0

    for match in results:
        for res in results[match]['winner']:
            if res != 'NA':
                print(res)
                if res == player:
                    count += 1
                winList.append(res)

    print(count / len(winList))

    cursor.close()
    userConnection.close()




def getOppWinrate(opponent):
    
    try:
        with open('python\playerName.txt', 'rb') as f:
            player = f.read().decode(encoding='utf-8', errors='replace')
    except:
        print('NA')
        return

    userConnection = sqlite3.connect("./database/mtgoAssist.db")
    cursor = userConnection.cursor()

    matches = cursor.execute("SELECT opponent, winner FROM matches ORDER BY opponent;").fetchall()


    #[[opponent, [name, name...]],[]]
    results = []
    for num, match in enumerate(matches):
        results.append([])
        for nom, item in enumerate(match):
            if nom == 0:
                results[num].append(json.loads(item)['players'][0])

            else:
                results[num].append(json.loads(item)['winner'])
            #results[num] = match[0]


    record = []

    while True:
        low = 0
        high = len(results) - 1
        mid = 0
    
        while low <= high:
    
            mid = (high + low) // 2
    
            # If x is greater, ignore left half
            if results[mid][0] < opponent:
                low = mid + 1
    
            # If x is smaller, ignore right half
            elif results[mid][0] > opponent:
                high = mid - 1
    
            # means x is present at mid
            else:
                for win in results[mid][1]:
                    record.append(win)
                results.pop(mid)
    
        # If we reach here, then the element was not present
        break

    count = 0
    for play in record:
        print(play)
        if play == player:
            count += 1

    print(count / len(record))


if __name__ == "main":
    pass
else:
    if sys.argv[1] == 'loaded':
        openData()
    elif sys.argv[1] == 'profile':
        getUserData()
    elif sys.argv[1] =='opponent':
        getOppWinrate(sys.argv[2])
    


