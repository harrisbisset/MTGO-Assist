import sqlite3
import urllib.request
import sys
from bs4 import BeautifulSoup
import requests


#datapull should run when program started with 'start parameter put in'


def checkConnection():
    host='https://mtgtop8.com/'
    try:
        urllib.request.urlopen(host)
        conInt = True
    except:
        conInt = False
    
    #check if userDB is created
    userConnection = sqlite3.connect("mtgoAssit.db")
    if connection.total_changes == 0:
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT database();")
            record = cursor.fetchone()

            #temp
            cursor.execute("DROP TABLE userDetails")
        except:
            cursor.execute("CREATE TABLE userDetails(name TEXT, mtgoName TEXT, mtgoPass TEXT)")
            sys.exit("createdDB")

    else:
        print("not connected to userDetails.db")

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
        print("Couldn't connect to local database")
    if connects[1] == True:
        page = requests.get('https://github.com/harrisbisset/MTGO-Assist/blob/main/README')
        soup = BeautifulSoup(page.content, 'html.parser')
        version = soup.find('td', id="LC3").text()
        if str(sys.args[2]).replace('v', '') != version:
            print("need to update")
    else:
        print("Not connected to the internet or mtgtop8 down")

    
    
if __name__ == "main":
    if str(sys.argv[1]) == 'loaded':
        openData()
#recordData
#int matchID, str(binary option = Limited/Contructed) gameType, str(binary option = ...) format, int tuple(W,D,L) record, str uDeck, str oDeck, str ozUsername, date, time
