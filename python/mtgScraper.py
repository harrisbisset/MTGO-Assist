from matchRecord import MatchRecord
from mtgtop8 import DriverController
import os

def main(path, player):
    fileList = [f for f in os.listdir(path) if f.endswith('.dat')]
    match = MatchRecord(player)
    dc = DriverController()
    for filename in fileList:
        decklists, date = match.run(f'{path}/{filename}')
        dc.returnDictNames(None, decklists, date)
    dc.quit()
    
    
    
if __name__ == '__main__':
    main('C:\Users\harri\AppData\Local\Apps\2.0\Data\JWMNX0QY.YK3\AGMD182G.AAW\mtgo..tion_92a8f782d852ef89_0003.0004_4d4c5524cb8c51a2\Data\AppFiles\E8BC386C00E942D40363482907EEDEEA', None)
