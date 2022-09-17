import sqlite3
import urllib.request
import sys
from bs4 import BeautifulSoup
import requests


def checkConnection():
    host='https://mtgtop8.com/'
    try:
        urllib.request.urlopen(host)
        conInt = True
    except:
        conInt = False
    
    userConnection = sqlite3.connect("./database/mtgoAssist.db")
    cursor = userConnection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='userDetails';")
    if not cursor.fetchone():
        cursor.execute("CREATE TABLE userDetails(temp TEXT);")

    #check if userDetails empty
    cursor.execute("select count(1) where exists (select * from userDetails)")
    check = cursor.fetchone()

    if check == (0,):
        print("unconnectedDB")
    else:
        print("connectedDB")
    return conInt


def openData():
    conInt = checkConnection()

    if conInt == True:
        print("connectedInt")
        page = requests.get('https://github.com/harrisbisset/MTGO-Assist/blob/main/README.md')
        soup = BeautifulSoup(page.content, 'html.parser')
        version = soup.find('p').text

        if str(sys.argv[2]) != version:
            print("updateProg")
    else:
        print("unconnectedInt")


def createUser():
    userConnection = sqlite3.connect("./database/mtgoAssist.db")
    cursor = userConnection.cursor()
    cursor.execute("DROP TABLE userDetails")
    cursor.execute("CREATE TABLE userDetails(name TEXT, pass TEXT, mtgoName TEXT, mtgoPass TEXT)")
    #print(f"INSERT INTO userDetails (name, pass, mtgoName, mtgoPass) VALUES ({v1}, {v2}, {v3}, {v4};")
    #cursor.execute(f"INSERT INTO userDetails (name, pass, mtgoName, mtgoPass) VALUES ({v1}, {v2}, {v3}, {v4});")
    params = (sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    cursor.execute(f"INSERT INTO userDetails (name, pass, mtgoName, mtgoPass) VALUES (?, ?, ?, ?);", params)
    print('createdUser')

#createUser("dw", "dwd2", "v3dwdw", "wddwv4")

if __name__ != "main":
    if str(sys.argv[1]) == 'loaded':
        openData()
    if str(sys.argv[1]) == 'createUser':
        createUser()
#recordData
#int matchID, str(binary option = Limited/Contructed) gameType, str(binary option = ...) format, int tuple(W,D,L) record, str uDeck, str oDeck, str ozUsername, date, time
