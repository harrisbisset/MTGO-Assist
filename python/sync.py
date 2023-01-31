import os
from os import walk
from mtgScraper import Scraper

#gets path of mtgo
localUser = os.getlogin()
path = f'C:\\Users\\{localUser}\\AppData\\Local\\Apps\\2.0\Data\\'

#gets next two folders and adds them to path
for i in range(0,2):
    folder = os.listdir(path)
    path = path + '\\' + folder[0]

#gets the main mtgo folders, they are prefixed by 'mtgo..tion_'
mainFolders = os.listdir(path)

scp = Scraper()

for folder in mainFolders:
    
    folderPath = path + '\\' + folder + '\\' + 'Data\\AppFiles'

    #gets the directories of the appfiles folder
    for (folderPath, directory, fileNames) in walk(folderPath):
        
        #.vs file may be in one of the directories, and is unnecessary
        if len(directory) > 1:
            directory.remove('.vs')
        
        #gets path of match files
        folderPath = folderPath + '\\' + directory[0]

        #don't look inside any subdirectory
        break
    
    scp.addPath(folderPath)


scp.run()
