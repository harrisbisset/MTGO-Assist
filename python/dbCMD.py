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
    
    #reformats
    for i, match in enumerate(matches):
        matches[i] = [json.dumps(match)]
    
    #sends data to renderer.js
    for count, i in enumerate(matches):
        if count == 2:
            pass
        else:
            print(i)



#gets user averages
def getUserData():
    userConnection = sqlite3.connect("../database/mtgoAssist.db")
    cursor = userConnection.cursor()
    

    cursor.close()
    userConnection.close()

openData()

# if __name__ == "main":
#     pass
# else:
#     if sys.argv[1] == 'loaded':
#         openData()
#     if sys.argv[1] == 'getProfileData':
#         getUserData()
