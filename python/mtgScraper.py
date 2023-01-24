from matchRecord import MatchRecord
from mtgtop8 import DriverController
import os.path
from datetime import datetime
import urllib.request
import sqlite3




def main(path):
    fileList = [f for f in os.listdir(path) if f.endswith('.dat')]

    #opens connection
    openConn()
    
    highestID = sqlliteGetID()
    top8Conn = checkInternet()
    
    #initilises modules
    match = MatchRecord()
    dc = DriverController()
    
    #loops through file list
    for filename in fileList:

        #gets decklists from MatchRecord
        #other stored data is implemented into database in MatchRecord
        decklists = match.getDecklists(f'{path}/{filename}')

        #if the file is valid
        if decklists is not None:
            highestID += 1
            
            #gets and reformats date
            x, y, z = datetime.fromtimestamp(os.path.getmtime(filename).split('/'))
            date = z + '/' + y + '/' + x

            if top8Conn == True:
                #gets the possible deck names from DriverController
                dictNames = dc.returnDictNames(None, decklists, date)

            #sends info to sqliite db
            sqlliteDriverData(highestID, date, dictNames)

    #closes webdriver
    dc.quit()
    
    #close connection
    closeConn()




def sqlliteGetID():
    #connects to and creates a record with the user's inputted information (from the dialog box)
    userConnection = sqlite3.connect("./database/mtgoAssist.db")
    cursor = userConnection.cursor()
    try:
        highestID = cursor.execute("SELECT MAX(matchID) FROM matches;")
    except:
        
        #creates formats table
        cursor.execute("CREATE TABLE formats(format TEXT NOT NULL PRIMARY KEY);")

        #inserts formats into the formats table
        formats = ['Standard', 'Pioneer', 'Modern', 'Legacy', 'Vintage']
        for elem in formats:
            cursor.execute(f"INSERT INTO formats(format) VALUES({elem});")

        #creates the matches table
        cursor.execute("""CREATE TABLE matches(
                            matchID INTEGER NOT NULL PRIMARY KEY, 
                            filename TEXT NOT NULL, 
                            players BLOB NOT NULL, 
                            decknames BLOB, 
                            decklistP1 BLOB NOT NULL, 
                            decklistP2 BLOB NOT NULL, 
                            firstTurns BLOB NOT NULL, 
                            winLoss BLOB, 
                            FOREIGN KEY(format) REFERENCES formats(formatName), 
                            type TEXT, 
                            date TEXT NOT NULL);""")

        cursor.execute("""CREATE TABLE games(
                            gamesID INTEGER NOT NULL PRIMARY KEY, 
                            FOREIGN KEY(matchID) REFERENCES matches(matchID) NOT NULL, 
                            gameNum INTEGER NOT NULL, 
                            gameLog TEXT NOT NULL, 
                            winner TEXT);""")

        #there are no records, so highestID is set to -1
        highestID = -1

    return highestID
    



def sqlliteDriverData(ID, date, dictNames):
    pass




def openConn():
    pass
    



def closeConn():
    pass




def checkInternet():

    #tries to open mtgtop8.com, if it can't then program will not open later
    host='https://mtgtop8.com/'
    try:
        urllib.request.urlopen(host)
        conInt = True
    except:
        conInt = False
    
    return conInt




if __name__ == '__main__':
    main('C:\Users\harri\AppData\Local\Apps\2.0\Data\JWMNX0QY.YK3\AGMD182G.AAW\mtgo..tion_92a8f782d852ef89_0003.0004_4d4c5524cb8c51a2\Data\AppFiles\E8BC386C00E942D40363482907EEDEEA', None)
