import pyautogui
import time
from PIL import Image, ImageDraw
#import psutil
#import subprocess
import sys
import os
import pygetwindow as gw
import urllib.request
import pytesseract
import cv2
import sqlite3

def main():

    #runs checkConnection(), and if false, it exits the program, returning 'unconnectdInt' to renderer.js
    if not checkConnection():
        print("unconnectedInt")
        exit
    
    if checkIfProcessRunning('MTGO.exe') == False:
        #MTGO is run from a .appref-ms (clickOnce) file, you can try to update this
        #openApplication()

        print("unOpened")
        exit

    else:
        #brings Main Navigation to foreground
        mainNavWin = gw.getWindowsWithTitle('Magic: The Gathering Online')[0]
        mainNavWin.activate()
        mainNavWin.maximize()

        #checks if endUserLicense.png present, if so, it exits asks user to close it
        checkEndUserLicense = pyautogui.locateOnScreen(r'.\images\endUserLicense.png')
        if checkEndUserLicense:
            print("license")
            exit

        #if user doesn't want to manually input data, logIN function is run
        logIN(mainNavWin)

        #navigate to settings
        while True:
            try:
                settingsLocation = pyautogui.locateOnScreen(r'.\images\settings.png', confidence=.70, region = (2435, 38, 52, 60))
                if settingsLocation is not None:
                    pyautogui.click(settingsLocation)
                    break
            finally:
                time.sleep(4)

        #navigate to game history
        gameHistLocation = pyautogui.locateOnScreen(r'.\images\game-history.png', confidence=.70, region = (0, 377, 292, 46))
        pyautogui.click(gameHistLocation)
        time.sleep(0.25)

        recordID = 0
        top = 368
        recordLoop = 0
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

        #while True:
        #for loops in range(0, 3):
        #takes screenshot of current record, each record is 40 tall
        pyautogui.screenshot('scrn.png', region=(285, top, 2000, 40))

        #gets data from screenshot and turns it into array
        imgText_rgb = cv2.imread('scrn.png')
        imgText_rgb = get_grayscale(imgText_rgb)
        record = pytesseract.image_to_string(imgText_rgb)

        #converts 12h to 24h time
        if record[6] == 'PM':
            temp = record[5].split(':')
            temp[0] = int(temp[0]) + 12
            record[5] = ':'.join(temp)
            record.remove(6)
        
        pyautogui.moveTo(400, top+20)
        details = pyautogui.locateOnScreen(r'.\images\details.png')
        pyautogui.click(details)
        time.sleep(0.5)
        
        games = list(pyautogui.locateAllOnScreen(r'.\images\replayGame.png'))
        #if not games:
            #break
        replayGone = False
        for game in games:
            pyautogui.click(game)
            gameNo = games.index(game) + 1
            while True:
                for eventWin in pyautogui.getAllWindows():
                    if 'Event' in eventWin.title:
                        eventWin.maximize()
                    else:
                        time.sleep(2)
                        notFound = pyautogui.locateOnScreen(r'.\images\notFound.png')
                        if notFound:
                            replayGone = True
                            break
            
            if replayGone == True:
                break
            
            

            print(gameNo)

            #get game data
            #MainB
            #SideB

            #os.system(f'./mtgtop8.py {gameNo} {record[1]} {MainB} {SideB} {record[5]}')
            #mtgtop8.com



            #each scroll moves down 3 records
            #recordLoop = recordLoop + 1
            #if recordLoop = 3:
                #top = 368
                #pyautogui.scroll(1)
            #top = top + 40
            #recordID = recordID + 1
            #pass














        pass


def checkIfProcessRunning(processName):
    #checks if application running
    print('Checking if application is running...')
    output = os.popen('wmic process get description').read()
    if processName in output:
        return True
    return False

def openApplication():
    #currently functionality non-existant, so error message instead
    return 

def logIN(mainNavWin):

    #sets autoFilled to false, first, for userName
    autoFilled = False
    #checks if it's on the login screen
    loginLocation = pyautogui.locateOnScreen(r'.\images\login.png', confidence=.65, region = (127, 673, 388, 117))

    #if true
    if loginLocation:
        try:
            password = pyautogui.locateOnScreen(r'.\images\password.png', confidence=.70, region = (122, 609, 399, 55))
            screenName = pyautogui.locateOnScreen(r'.\images\screenName.png', confidence=.70, region = (122, 556, 400, 54))
            uN = '-Sire'
        except:
            #if program can't detect screenName, but login detected, screenName is autoFilled
            autoFilled = True
            pass
        
        uP = 'DeathTouch159'

        #workaround for problem that occurs when .activate() doesn't work and throws [Error code from Windows: 6 - The handle is invalid.]
        if mainNavWin != []:
            try:
                mainNavWin.activate()
            except:
                mainNavWin.minimize()
                mainNavWin.maximize()
        mainNavWin.activate()

        #asks field data, and inputs it
        if autoFilled == False:
            userNamePass(screenName, uN)
        userNamePass(password, uP)
        pyautogui.click(loginLocation)
    else:
        return

def userNamePass(button, inputData):
    pyautogui.click(button)
    pyautogui.press('backspace', presses=26)
    pyautogui.write(inputData)


def checkConnection(host='http://google.com'):
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False


def ocr_core(img):
    text = pytesseract.image_to_string(img)
    return text

def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def remove_noise(image):
    return cv2.medianBlur(image, 5)

def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


main()
