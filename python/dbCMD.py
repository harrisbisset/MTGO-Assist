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
    
            if results[mid][0] < opponent:
                low = mid + 1
            elif results[mid][0] > opponent:
                high = mid - 1
            else:
                for win in results[mid][1]:
                    record.append(win)
                results.pop(mid)
    
        #element not present
        break

    count = 0
    for play in record:
        if play == player:
            count += 1

    if count != 0:
        print(count / len(record))
    else:
        print(count)

#getOppWinrate('Pazmaster')

if __name__ == "main":
    pass
else:
    if sys.argv[1] == 'loaded':
        openData()
    elif sys.argv[1] == 'profile':
        getUserData()
    elif sys.argv[1] =='opponent':
        getOppWinrate(sys.argv[2])
    


