from matchRecord import MatchRecord
from mtgtop8 import DriverController
import os.path
from datetime import datetime
import urllib.request
import sqlite3


class Scraper():
    def __init__(self):
        self.paths = []

    def addPath(self, path):
        
        #adds path to object
        self.paths.append(path)
        
    def run(self):

        #opens connection
        self.openConn()

        #checks if database exists
        self.checkDB()

        top8Conn = self.checkInternet()
            
        #initilises modules
        match = MatchRecord()
        dc = DriverController()
        
        for path in self.paths:
            
            #gets list of files in path
            fileList = [f for f in os.listdir(path) if f.endswith('.dat')]
            
            #gets list of files in database
            self.cursor.execute("SELECT filename FROM matches;")
            filenames = self.cursor.fetchall()

            #loops through file list
            for filename in fileList:

                #if file already scraped
                if filename in filenames:
                    break
                
                #gets decklists from MatchRecord
                #other stored data is implemented into database in MatchRecord
                decklists, extra, matchlog, players = match.getDecklists(f'{path}/{filename}')

                #if the file is valid
                if decklists is not None:
                    
                    #gets and reformats date
                    dateTime = str(datetime.fromtimestamp(os.path.getmtime(path + '\\' + filename)))
                    x, y, z = dateTime.split(' ')[0].split('-')
                    date = z + '/' + y + '/' + x

                    if top8Conn == True:
                        #gets the possible deck names from DriverController
                        dictNames = dc.returnDictNames(decklists, date)
                    else:
                        dictNames = "NA"
                        
                    #sends info to sqliite db
                    self.sqlliteDriverData(filename, date, dictNames, extra, decklists, players, matchlog)

        #closes webdriver
        dc.quit()
            
        #close connection
        self.closeConn()
        



    def openConn(self):
        self.userConnection = sqlite3.connect("./database/mtgoAssist.db")
        self.cursor = self.userConnection.cursor()
        # self.userConnection.execute("PRAGMA foreign_keys = 1")




    def checkInternet(self):

        #tries to open mtgtop8.com, if it can't then program will not open later
        host='https://mtgtop8.com/'
        try:
            urllib.request.urlopen(host)
            conInt = True
        except:
            conInt = False
        
        return conInt




    def checkDB(self):
        try:
            return self.cursor.execute("SELECT MAX(matchID) FROM matches;")
        except:

            #creates the matches table
            self.cursor.execute("""CREATE TABLE matches(
                                matchID INTEGER PRIMARY KEY, 
                                filename TEXT, 
                                players TEXT NOT NULL, 
                                decknames TEXT, 
                                decklistP1 TEXT NOT NULL, 
                                decklistP2 TEXT NOT NULL, 
                                firstTurns TEXT NOT NULL, 
                                winLoss TEXT NOT NULL, 
                                format TEXT, 
                                type TEXT, 
                                date TEXT NOT NULL);""")
            self.userConnection.commit()

            #creates games table
            self.cursor.execute("""CREATE TABLE games(
                                gamesID INTEGER NOT NULL PRIMARY KEY, 
                                gameNum INTEGER NOT NULL,
                                startingHands TEXT NOT NULL,
                                gameLog TEXT NOT NULL, 
                                winner TEXT, 
                                matchID INTEGER REFERENCES matches(matchID) ON UPDATE CASCADE);""")
            self.userConnection.commit()
        return 
        



    def sqlliteDriverData(self, filename, dateTime, dictNames, extra, decklists, players, matchlog):
        #inserts match into database

        data = (filename, str(players), str(dictNames), str(decklists[0]), str(decklists[1]), str(extra['play']), str(extra['winner']), 'NA', 'Constructed', dateTime)

        self.cursor.execute("INSERT INTO matches(filename, players, decknames, decklistP1, decklistP2, firstTurns, winLoss, format, type, date) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", data)
        self.userConnection.commit()
        self.cursor.execute("SELECT MAX(matchID) FROM matches;")
        matchID = self.cursor.fetchone()

        #inserts games into database
        for gameNo, game in enumerate(matchlog):
            data = (int(matchID[0]), str(matchlog.index(game)), str(extra['startingHands']), str(matchlog[gameNo]), str(extra['winner'][matchlog.index(game)]))
            self.cursor.execute("INSERT INTO games(matchID, gameNum, startinghands, gameLog, winner)  VALUES(?,?,?,?,?);", data)
                                                
                                                        


    def closeConn(self):
        self.userConnection.commit()
        self.cursor.close()
        self.userConnection.close()
