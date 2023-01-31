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
        self.paths.append(path)
        
    def run(self):
        for path in self.paths:
            fileList = [f for f in os.listdir(path) if f.endswith('.dat')]

            #opens connection
            self.openConn()

            #checks if database exists
            self.checkDB()
            
            top8Conn = self.checkInternet()
            
            #initilises modules
            match = MatchRecord()
            dc = DriverController()
            
            #loops through file list
            for filename in fileList:

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
        self.userConnection.execute("PRAGMA foreign_keys = 1")




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
            self.cursor.execute("SELECT MAX(matchID) FROM matches;")
        except:
            
            #creates formats table
            self.cursor.execute("CREATE TABLE formats(format TEXT NOT NULL PRIMARY KEY);")
            self.userConnection.commit()

            #inserts formats into the formats table
            formats = ['Standard', 'Pioneer', 'Modern', 'Legacy', 'Vintage', 'NA']
            for elem in formats:
                self.cursor.execute(f"INSERT INTO formats(format) VALUES('{elem}');")
            self.userConnection.commit()

            #creates the matches table
            self.cursor.execute("""CREATE TABLE matches(
                                matchID INTEGER NOT NULL PRIMARY KEY, 
                                filename TEXT NOT NULL, 
                                players BLOB NOT NULL, 
                                decknames BLOB, 
                                decklistP1 BLOB NOT NULL, 
                                decklistP2 BLOB NOT NULL, 
                                firstTurns BLOB NOT NULL, 
                                winLoss BLOB, 
                                format REFERENCES formats(format), 
                                type TEXT, 
                                date TEXT NOT NULL);""")
            self.userConnection.commit()

            #creates games table
            self.cursor.execute("""CREATE TABLE games(
                                gamesID INTEGER NOT NULL PRIMARY KEY, 
                                matchID REFERENCES matches(matchID) NOT NULL, 
                                gameNum INTEGER NOT NULL,
                                startingHands BLOB NOT NULL,
                                gameLog TEXT NOT NULL, 
                                winner TEXT);""")
            self.userConnection.commit()

        



    def sqlliteDriverData(self, filename, dateTime, dictNames, extra, decklists, players, matchlog):
        gameFormat = 'NA'
        gameType = 'Constructed'
        print(players)
        print(extra)
        print(filename)
        #inserts match into database
        print(f"INSERT INTO matches(filename, players, decknames, decklistP1, decklistP2, firstTurns, winLoss, format, type, date) VALUES('{filename}', '{players}', '{dictNames}', '{decklists[0]}', '{decklists[1]}', '{extra['play']}', '{extra['winner']}', NA, Constructed, '{dateTime}');")
        #self.cursor.execute(f"INSERT INTO matches(filename, players, decknames, decklistP1, decklistP2, firstTurns, winLoss, format, type, date) VALUES('{filename}', '{players}', '{dictNames}', '{decklists[0]}', '{decklists[1]}', '{extra['play']}', '{extra['winner']}', NA, Constructed, '{dateTime}');")

        self.cursor.execute(f'''INSERT INTO matches(filename, players, decknames, 
                                                    decklistP1, decklistP2, firstTurns, 
                                                    winLoss, format, type, date) 
                                                    
                                                    VALUES('{filename}', '{players}', '{dictNames}', 
                                                    '{decklists[0]}', '{decklists[1]}', '{extra['play']}', 
                                                    '{extra['winner']}', '{gameFormat}', '{gameType}', '{dateTime}');''')
        self.userConnection.commit()

        matchID = self.cursor.execute("SELECT MAX(matchID) FROM matches;")

        #inserts games into database
        for game in matchlog:
            self.cursor.execute(f"""INSERT INTO games(matchID, gameNum, startinghands, gameLog, winner) 
                                                
                                                        VALUES('{matchID}', '{matchlog.index(game)}', '{extra['startingHands']}','{matchlog[game]}', 
                                                        '{extra['winner'][matchlog.index(game)]}');""")

    


    def closeConn(self):
        self.userConnection.commit()
        self.cursor.close()
        self.userConnection.close()





if __name__ == '__main__':
    Scraper(r'C:\Users\harri\AppData\Local\Apps\2.0\Data\JWMNX0QY.YK3\AGMD182G.AAW\mtgo..tion_92a8f782d852ef89_0003.0004_4d4c5524cb8c51a2\Data\AppFiles\E8BC386C00E942D40363482907EEDEEA')
