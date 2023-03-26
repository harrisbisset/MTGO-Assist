from matchRecord import MatchRecord
from mtgtop8 import DriverController
import os.path
from datetime import datetime
import urllib.request
import sqlite3
import json
import re



class Scraper():
    def __init__(self):
        self.paths = []
        self.player = ''

    


    def getPlayer(self, filename):
        
        try:
            with open('./playerName.txt', 'rb') as f:
                self.player = f.read().decode(encoding='utf-8', errors='replace')
        except:
            #reads file contents
            with open(filename, 'rb') as f:
                file = f.read().decode(encoding='utf-8', errors='replace').replace(' ', '').splitlines()
            
            #gets player name from file contents
            self.player = re.findall('"(.*)"', file[file.index('Setting="LastLoginName"')+1])[0]




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
        
        #gets list of files in database
        self.cursor.execute("SELECT filename FROM matches;")
        filenames = self.cursor.fetchall()
        filenames = [json.loads(i[0])['filename'] for i in filenames]

        for path in self.paths:
            
            #gets list of files in path
            fileList = [f for f in os.listdir(path) if f.endswith('.dat')]

            #loops through file list
            for filename in fileList:

                #if file already scraped
                if filename in filenames:
                    continue
                
                #gets decklists from MatchRecord
                #other stored data is implemented into database in MatchRecord
                decklists, extra, players = match.getDecklists(f'{path}/{filename}')

                #if the file is valid
                if decklists != {} and decklists is not None:
                    players.remove(self.player)

                    #gets and reformats date
                    dateTime = str(datetime.fromtimestamp(os.path.getmtime(path + '\\' + filename)))
                    x, y, z = dateTime.split(' ')[0].split('-')
                    date = {'date':f'{z}/{y}/{x}'}
                    
                    if top8Conn == True:
                        #gets the possible deck names from DriverController
                        deckName, matchLists = dc.returnDeckName(decklists, date)
                    else:
                        deckName = {'NA': 1.0}
                    
                    #sends info to sqliite db
                    self.sqlliteDriverData({'filename':filename}, dateTime, deckName, extra, {'players':players}, matchLists)


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
                                filename BLOB NOT NULL, 
                                opponent BLOB NOT NULL, 
                                decknames BLOB, 
                                decklistP1 BLOB, 
                                decklistP2 BLOB, 
                                play BLOB NOT NULL,
                                winner BLOB NOT NULL,
                                date BLOB NOT NULL);""")
            self.userConnection.commit()

        


    def sqlliteDriverData(self, filename, dateTime, deckName, extra, players, matchLists):

        #inserts match into database
        data = (json.dumps(filename), json.dumps(players), json.dumps(deckName), json.dumps({'P1':matchLists['P1']}), json.dumps({'P2':matchLists['P2']}), json.dumps({'play':extra['play']}), json.dumps({'winner':extra['winner']}), json.dumps({'date':dateTime}))
        
        self.cursor.execute("INSERT INTO matches(filename, opponent, decknames, decklistP1, decklistP2, play, winner, date) VALUES(?,?,?,?,?,?,?,?,?,?);", data)
        self.userConnection.commit()
            
            


    def closeConn(self):
        self.userConnection.commit()
        self.cursor.close()
        self.userConnection.close()
