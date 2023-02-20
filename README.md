## MTGO Assistant Tool
v1.0.0

## License
[MIT License](LICENSE)


96.5h spent programming

        #format is currently not discerable from the logs, so this should always be true
        if format is not None:
            #finds the format <select> tag, and selects the format passed in
            selectElement = self.driver.find_element(By.XPATH, '//body/div/div/table/tbody/tr/td[1]/form/table/tbody/tr[4]/td[2]/select')
            selectObject = Select(selectElement)
            selectObject.select_by_visible_text(format)

# #creates games table
            # self.cursor.execute("""CREATE TABLE games(
            #                     gamesID INTEGER NOT NULL PRIMARY KEY, 
            #                     gameNum INTEGER NOT NULL,
            #                     startingHands BLOB NOT NULL,
            #                     decklistP1 BLOB,
            #                     decklistP2 BLOB,
            #                     gameLog BLOB NOT NULL, 
            #                     winner BLOB, 
            #                     matchID INTEGER REFERENCES matches(matchID) ON UPDATE CASCADE);""")
            # self.userConnection.commit()
            

# self.cursor.execute("SELECT MAX(matchID) FROM matches;")
        # matchID = self.cursor.fetchone()

        # #inserts games into database
        # for gameNo in range(1,len(matchlog)+1):
        #     data = (matchID[0], gameNo, json.dumps({'startingHands':extra['startingHands']}), json.dumps(decklists[gameNo][players['players'][1]]), json.dumps(decklists[gameNo][players['players'][0]]), json.dumps(matchlog[gameNo]), json.dumps(extra['winner'][gameNo-1]))
        #     self.cursor.execute("INSERT INTO games(matchID, gameNum, startingHands, decklistP1, decklistP2, gameLog, winner)  VALUES(?,?,?,?,?,?,?);", data)
