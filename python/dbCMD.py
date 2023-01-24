import urllib.request
import sys


def checkConnection():

    #tries to open mtgtop8.com, then sends the back to the renderer.js
    host='https://mtgtop8.com/'
    try:
        urllib.request.urlopen(host)
        conInt = True
    except:
        conInt = False
    
    return conInt


if __name__  != "main":
    if sys.argv[1] == 'checkConnection':
        checkConnection()
