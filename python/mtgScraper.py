from matchRecord import MatchRecord
from mtgtop8 import DriverController
import os.path
from datetime import datetime

def main(path, player):
    fileList = [f for f in os.listdir(path) if f.endswith('.dat')]

    #initilises modules
    match = MatchRecord(player)
    dc = DriverController()

    #loops through file list
    for filename in fileList:

        #gets decklists from MatchRecord
        decklists, matchLog, gameRecord, onPlay, startingHands = match.getDecklists(f'{path}/{filename}')

        #if the file is valid
        if decklists is not None:
            
            #gets and reformats date
            x, y, z = datetime.fromtimestamp(os.path.getmtime(filename).split('/'))
            date = z + '/' + y + '/' + x

            #gets the possible deck names from DriverController
            dictNames = dc.returnDictNames(None, decklists, date)

            #sends info to sqliite db
            sqllite(decklists, date, dictNames)

    #closes webdriver
    dc.quit()
    
def sqllite(decklists, date, dictNames, matchLog, gameRecord, onPlay, startingHands):
    pass


if __name__ == '__main__':
    main('C:\Users\harri\AppData\Local\Apps\2.0\Data\JWMNX0QY.YK3\AGMD182G.AAW\mtgo..tion_92a8f782d852ef89_0003.0004_4d4c5524cb8c51a2\Data\AppFiles\E8BC386C00E942D40363482907EEDEEA', None)
