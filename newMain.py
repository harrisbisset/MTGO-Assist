import pyautogui
import time
#from PIL import Image, ImageDraw
import psutil
#import subprocess
#import sys
import os
import pygetwindow as gw

def main():
    print(os.getcwd())
    if checkIfProcessRunning('MTGO.exe') == False:
        #MTGO is run from a .appref-ms (clickOnce) file, you can try to update this
        openApplication()
    else:
        #brings Main Navigation to foreground
        mainNavWin = gw.getWindowsWithTitle('Magic: The Gathering Online')[0]
        mainNavWin.activate()
        mainNavWin.maximize()

        #checks if signed, if not, signs in
        logIN(mainNavWin)

        #navigate to settings
        

        #click on settings
        #navigate to game history
        #click on game history
        #navigate to top of records
        #while recordID != None:
            #select next record
            #get data
            #navigate to replays
            #for replay in replays:
                #click on replay
                #if open app:
                    #record data
                #else:
                    #break

            #send data for record to imGui
        pass


def checkIfProcessRunning(processName):
    #Checks if process running
    print('Checking if application is running...')
    output = os.popen('wmic process get description').read()
    if processName in output:
        return True
    return False

def openApplication():
    #currently functionality non-existant, so error message instead
    #send error message to imGui
    return 

def logIN(mainNavWin):
    #sets autoFilled to false, first, for userName
    autoFilled = False
    #checks if it's on the login screen
    loginLocation = pyautogui.locateOnScreen(r'C:\Users\harri\OneDrive\Documents\mtgoAddon\images\login.png', confidence=.65, region = (127, 673, 388, 117))

    #if true
    if loginLocation:
        try:
            password = pyautogui.locateOnScreen(r'C:\Users\harri\OneDrive\Documents\mtgoAddon\images\password.png', confidence=.70, region = (122, 609, 399, 55))
            screenName = pyautogui.locateOnScreen(r'C:\Users\harri\OneDrive\Documents\mtgoAddon\images\screenName.png', confidence=.70, region = (122, 556, 400, 54))
            uN = input("Username: ")
        except:
            #if program can't detect screenName, but login detected, screenName is autoFilled
            autoFilled = True
            pass
        
        uP = input("Password: ")

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
    pyautogui.press('backspace', presses=25)
    pyautogui.write(inputData)



main()
