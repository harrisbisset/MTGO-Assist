from matchRecord import MatchRecord
from mtgtop8 import DriverController
import os.path
from datetime import datetime
import urllib.request
import sqlite3
import json


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
                    date = {'date':f'{z}/{y}/{x}'}
                    
                    if top8Conn == True:
                        #gets the possible deck names from DriverController
                        deckName, matchLists = dc.returnDeckName(decklists, date)
                    else:
                        deckName = "NA"
                    
                    
                    #sends info to sqliite db
                    self.sqlliteDriverData({'filename':filename}, dateTime, deckName, extra, decklists, {'players':players}, matchlog, matchLists)


        #closes webdriver
        dc.quitDc()
            
        #close connection
        self.closeConn()
        



    def openConn(self):
        self.userConnection = sqlite3.connect("./database/mtgoAssist.db")
        self.cursor = self.userConnection.cursor()




    def checkInternet(self):

        #tries to open mtgtop8.com, if it can't then program will not open later
        url = 'https://mtgtop8.com/'
        try:
            urllib.request.urlopen(url)
            conInt = True
        except:
            conInt = False
        
        return conInt



    def checkDB(self):
        try:
            self.cursor.execute("SELECT MAX(matchID) FROM matches;")
        except:

            #creates the matches table
            self.cursor.execute("""CREATE TABLE matches(
                                matchID INTEGER PRIMARY KEY, 
                                filename BLOB, 
                                players BLOB NOT NULL, 
                                decknames BLOB, 
                                decklistP1 BLOB, 
                                decklistP2 BLOB, 
                                play BLOB NOT NULL,
                                winner BLOB NOT NULL,
                                format BLOB, 
                                type BLOB, 
                                date BLOB NOT NULL);""")
            self.userConnection.commit()

            #creates games table
            self.cursor.execute("""CREATE TABLE games(
                                gamesID INTEGER NOT NULL PRIMARY KEY, 
                                gameNum INTEGER NOT NULL,
                                startingHands BLOB NOT NULL,
                                decklistP1 BLOB,
                                decklistP2 BLOB,
                                gameLog BLOB NOT NULL, 
                                winner BLOB, 
                                matchID INTEGER REFERENCES matches(matchID) ON UPDATE CASCADE);""")
            self.userConnection.commit()
        



    def sqlliteDriverData(self, filename, dateTime, deckName, extra, decklists, players, matchlog, matchLists):

        #inserts match into database
        data = (json.dumps(filename), json.dumps(players), json.dumps(deckName), json.dumps({'P1':matchLists['P1']}), json.dumps({'P2':matchLists['P2']}), json.dumps({'play':extra['play']}), json.dumps({'winner':extra['winner']}), json.dumps({'format':'NA'}), json.dumps({'type':'Constructed'}), json.dumps({'date':dateTime}))
        
        self.cursor.execute("INSERT INTO matches(filename, players, decknames, decklistP1, decklistP2, play, winner, format, type, date) VALUES(?,?,?,?,?,?,?,?,?,?);", data)
        self.userConnection.commit()
        
        self.cursor.execute("SELECT MAX(matchID) FROM matches;")
        matchID = self.cursor.fetchone()

        #inserts games into database
        for gameNo in range(1,len(matchlog)):
            data = (matchID[0], gameNo, json.dumps({'startingHands':extra['startingHands']}), json.dumps(decklists[gameNo][players['players'][1]]), json.dumps(decklists[gameNo][players['players'][0]]), json.dumps(matchlog[gameNo]), json.dumps(extra['winner'][gameNo-1]))
            self.cursor.execute("INSERT INTO games(matchID, gameNum, startingHands, decklistP1, decklistP2, gameLog, winner)  VALUES(?,?,?,?,?,?,?);", data)
            
            


    def closeConn(self):
        self.userConnection.commit()
        self.cursor.close()
        self.userConnection.close()
