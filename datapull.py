import sqlite
import mysql.connector
from mysql.connector import Error

#datapull should run when program started with 'start parameter put in'

function main(param):
    if param == openData:
        pass
    elif param == install:
        setup()

def checkConnection():
    try:
        urllib.request.urlopen(host)
        conInt = True
    except:
        conInt = False
  
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='#########',
                                             user='#########',
                                             password='######')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
            conDB = True
    except Error as e:
        print("Error while connecting to MySQL", e)
        conDB = False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    return conDB, conInt

def setup():
    pass

    

def openData():
    connects = checkConnection()
    if connects[0] == True:
        pass

    
    
    
main(param)
