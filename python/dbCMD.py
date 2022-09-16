import sqlite3
import urllib.request
import sys
from bs4 import BeautifulSoup
import requests
import os


#datapull should run when program started with 'start parameter put in'


def checkConnection():
    host='https://mtgtop8.com/'
    try:
        urllib.request.urlopen(host)
        conInt = True
    except:
        conInt = False
    
    

    #check if userDB is created
    if os.path.isfile('./database/mtgoAssit.db'):
        print("connectedDB")
    else:
        userConnection = sqlite3.connect("./database/mtgoAssit.db")
        cursor = userConnection.cursor()
        cursor.execute("CREATE TABLE userDetails(name TEXT, mtgoName TEXT, mtgoPass TEXT)")
        # cursor.execute("DROP TABLE userDetails")
        print("createdDB")
   

    

    # else:
    #     print("not connected to userDetails.db")

    connection = sqlite3.connect("########.db")
    if connection.total_changes == 0:
        conDB = True
    else:
        conDB = False

    return conDB, conInt


def openData():
    connects = checkConnection()
    if connects[0] == True:
        #get data
        pass
    else:
        print("unconnectedDB")
    if connects[1] == True:
        print("connectedInt")
        page = requests.get('https://github.com/harrisbisset/MTGO-Assist/blob/main/README.md')
        soup = BeautifulSoup(page.content, 'html.parser')
        version = soup.find('p').text

        if str(sys.argv[2]) != version:
            print("updateProg")
    else:
        print("unconnectedInt")

if __name__ != "main":
    #if str(sys.argv[1]) == 'loaded':
    openData()
#recordData
#int matchID, str(binary option = Limited/Contructed) gameType, str(binary option = ...) format, int tuple(W,D,L) record, str uDeck, str oDeck, str ozUsername, date, time
