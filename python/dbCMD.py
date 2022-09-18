import sqlite3
import urllib.request
import sys
from bs4 import BeautifulSoup
import requests


def checkConnection():

    #tries to open mtgtop8.com, then sends the back to the renderer.js
    host='https://mtgtop8.com/'
    try:
        urllib.request.urlopen(host)
        conInt = True
    except:
        conInt = False
    
    #opens/creates mtgoAssist.db
    userConnection = sqlite3.connect("./database/mtgoAssist.db")
    cursor = userConnection.cursor()

    #if db empty, it creates a temporary userDetails table
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='userDetails';")
    if not cursor.fetchone():
        cursor.execute("CREATE TABLE userDetails (temp TEXT);")
        userConnection.commit()


    #check if userDetails empty
    cursor.execute("select count(1) where exists (select * from userDetails)")
    check = cursor.fetchone()

    #if sends result if empty back to renderer.js
    if check == (0,):
        print("unconnectedDB")
    else:
        print("connectedDB")

    cursor.close()
    userConnection.close()
    return conInt


def openData():
    conInt = checkConnection()

    #if python was able to connect to mtgtop8.com
    if conInt == True:
        print("connectedInt")

        #it opens the github repository, and checks if the version listed in the readme.md file is the same as the one stored in the package.json file
        page = requests.get('https://github.com/harrisbisset/MTGO-Assist/blob/main/README.md')
        soup = BeautifulSoup(page.content, 'html.parser')
        version = soup.find('p').text

        #if the package.json file isn't the same as the one in the github file, it sends that information back to renderer.js
        if sys.argv[2] != version.replace('v',''):
            print("updateProg")
    else:
        print("unconnectedInt")


def createUser():

    #connects to and creates a record with the user's inputted information (from the dialog box)
    userConnection = sqlite3.connect("./database/mtgoAssist.db")
    cursor = userConnection.cursor()
    cursor.execute("DROP TABLE userDetails")
    cursor.execute("CREATE TABLE userDetails(name TEXT, pass TEXT, mtgoName TEXT, mtgoPass TEXT)")
    params = (sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    query = ("INSERT INTO userDetails VALUES (?, ?, ?, ?)")
    cursor.execute(query, params)
    userConnection.commit()
    cursor.close()
    userConnection.close()
    print('createdUser')

if __name__ == "main":
    pass
else:
    if str(sys.argv[1]) == 'loaded':
        openData()
    if str(sys.argv[1]) == 'createUser':
        createUser()
#recordData
#int matchID, str(binary option = Limited/Contructed) gameType, str(binary option = ...) format, int tuple(W,D,L) record, str uDeck, str oDeck, str ozUsername, date, time
