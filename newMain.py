import pyautogui
import time
#from PIL import Image, ImageDraw
import psutil
import os

def checkIfProcessRunning(processName):
  '''Check if there are any running process that contains the given name processName.
  Iterate over the all the running process'''
  print('Checking if application is running...')
  for proc in psutil.process_iter():
    try:
      #Check if process name contains the given name string
      if processName.lower() in proc.name().lower():
        return True
      except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass
      return False

def Application(uN, uP):
  os.system(Magic The Gathering Online")
  return pass
      
      
#checks if app open, if not, opens app, input's user's username and password
if checkIfProcessRunning('main navigation') == False:
  userName = input("Input Username: ")
  userPass = input("Input Password: ")
  openApplication(userName, userPass)
else:
  pass
