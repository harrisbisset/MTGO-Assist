import sqlite3
import sys
import json

#gets data from database to be displayed on table
def openData():
    userConnection = sqlite3.connect("./data/mtgoAssist.db")
    cursor = userConnection.cursor()
    try:
        matches = cursor.execute("SELECT * FROM matches ORDER BY matchID DESC;").fetchall()
        closeConn(cursor, userConnection)

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

    userConnection = sqlite3.connect("./data/mtgoAssist.db")
    cursor = userConnection.cursor()

    matches = cursor.execute("SELECT winner FROM matches;").fetchall()
    closeConn(cursor, userConnection)

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




def getOppWinrate(opponent):
    
    try:
        with open('data/playerName.txt', 'rb') as f:
            player = f.read().decode(encoding='utf-8', errors='replace')
    except:
        print('NA')
        return

    userConnection = sqlite3.connect("./data/mtgoAssist.db")
    cursor = userConnection.cursor()
    
    vals = (json.dumps({"players":[f"{opponent}"]}),)

    matches = cursor.execute(f"SELECT COUNT(matchID) FROM matches WHERE opponent = ?;", vals).fetchone()[0]

    closeConn(cursor, userConnection)
    print(matches)




def closeConn(cursor, userConnection):
    cursor.close()
    userConnection.close()



if __name__ == "main":
    pass
else:
    if sys.argv[1] == 'loaded':
        openData()
    elif sys.argv[1] == 'profile':
        getUserData()
    elif sys.argv[1] =='opponent':
        getOppWinrate(sys.argv[2])
    

