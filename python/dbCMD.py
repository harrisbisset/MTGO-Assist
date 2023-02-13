import sqlite3
import sys
import json

#gets data from database to be displayed on table
def openData():
    userConnection = sqlite3.connect("./database/mtgoAssist.db")
    cursor = userConnection.cursor()

    matches = cursor.execute("SELECT * FROM matches ORDER BY matchID DESC limit 20;").fetchall()

    cursor.close()
    userConnection.close()
    
    results = {}

    for matchTuple in matches:
        results[matchTuple[0]] = [{}]
        for data in matchTuple:
            if isinstance(data, int) == False:
                data = json.loads(data)
                results[matchTuple[0]][0][list(data.keys())[0]] = data[list(data.keys())[0]]
                
    print(json.dumps(results))



#gets user averages
def getUserData():
    userConnection = sqlite3.connect("../database/mtgoAssist.db")
    cursor = userConnection.cursor()
    

    cursor.close()
    userConnection.close()

if __name__ == "main":
    pass
else:
    if sys.argv[1] == 'loaded':
        openData()
    if sys.argv[1] == 'getProfileData':
        getUserData()
