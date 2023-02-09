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

    for match in matches:
        for i, item in enumerate(match):
            if i == 2:
                print(item[0])
                print(item[1])
            if i == 3:
                print(item.key(0))
                print(item[0])
                print(item.key(1))
                print(item[1])
            else:
                print(item)



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
