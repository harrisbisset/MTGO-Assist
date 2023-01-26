import re

class MatchRecord:

    def __init__(self):
        pass


    def getDecklists(self, filename):
        decklists = []
        extra = {'play':[], 'startingHands':[], 'winner':[]}

        #gets matchLog
        with open(filename, 'rb') as f:
            #unknown characters are replaced by \ufffd (those question marks)
            self.matchLog = f.read().decode(encoding='utf-8', errors='replace')

        #tries to create self.players
        try:
            self.getPlayers()
            #if there is a problem reading the player names or the match is not 1v1 (fie invalid)
        except (IndexError, ValueError):
            return None, None, None, None

        #formats self.matchLog
        self.formatLines()

        #if there are less than 2 games, it's not a complete match
        if len(self.matchLog) < 2:
            return None, None, None, None


        #loops through each game
        for game in self.matchLog:
            if not game:
                break
            
            #gets decklists from game
            gameDecklists = self.getDeckLists(game)
            if decklists is None:
                return None, None, None, None
            decklists.append(gameDecklists)

            try:
                extra['play'].append(self.getOnPlay(game))
            except:
                extra['play'].append('unknown')
            
            try:
                extra['startingHands'].append(self.getStartingHands(game))
            except:
                extra['startingHands'] = 'unknown'
            
            extra['winner'].append(self.getWinner(game))

        return decklists, extra, self.matchLog, self.players




    def getPlayers(self):
        #finds all players
        players = re.compile('@P(\S+) rolled').findall(self.matchLog)
        
        #the first player in the game log is always the user
        self.players = list(players)



    def formatLines(self):
        #formats self.matchLog in [['random text', 'random text', 'player rolled', 'player rolled'], [game 1], [game 2...]] and removes noise
        
        #removes all non-ascii characters and some non-random characters
        filteredMatch = re.split(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff\ufffd\.\{\}\|\\=#\^><$]', self.matchLog)
        filteredMatch = [re.sub('^.*@P', '@P', line) for line in filteredMatch if len(line) > 4]
        
        #splits by game
        txt = ' '.join(filteredMatch)
        regex = f'@P{self.players[0]} joined the game @P{self.players[1]} joined the game'
        filteredMatch = re.compile(regex).split(txt)

        #splits by turn
        regex = f'Turn [1-9]: {self.players[0]}|Turn [1-9]: {self.players[1]}|Turn [1-5][0-9]: {self.players[0]}|Turn [1-5][0-9]: {self.players[0]}'
        filteredMatch = [re.compile(regex).split(turn) for turn in filteredMatch]
        
        #removes last random characters
        filteredMatch = [[re.split('(@P)', turn) for turn in game] for game in filteredMatch]
        filteredMatch = [[[re.sub(r'@P|[^\x00-\x7F]', '', line) for line in turn if len(line) > 4] for turn in game] for game in filteredMatch]
        
        del filteredMatch[0]
        self.matchLog = filteredMatch




    def getDeckLists(self, game):
        decklists = {self.players[0]: dict(), self.players[1]: dict()}

        #stores cards each player has played, revealed, discarded, cycled
        #game actions are formatted as @P(player_name) (casts|plays|discards|cycles|reveals)
        #card names are formatted as @[Card Name@:numbers,numbers:@]
        playCardPattern = re.compile(f'({self.players[0]}|{self.players[1]}) (casts|plays|discards|cycles) (@\[([a-zA-Z\s,-]+)@:[0-9,]+:@\])')
        revealedCardPattern = re.compile(f'({self.players[0]}|{self.players[1]}) (reveals) (@\[([a-zA-Z\s,-]+)@:[0-9,]+:@\])')

        for turn in game:
            #finds matched patterns
            playCardMatches = playCardPattern.findall(' '.join(turn))
            revealedMatches = revealedCardPattern.findall(' '.join(turn))


            for actions in playCardMatches:

                #if a card has been revealed, and has interacted with the game, remove it from revealedMatches
                if actions[3] in revealedMatches:
                    revealedMatches.pop(revealedMatches.index(actions[3]))

                #adds card to decklists
                if actions[3] in decklists[actions[0]]:
                    decklists[actions[0]][actions[3]] += 1
                else:
                    decklists[actions[0]].update({actions[3]:1})


            for revealed in revealedMatches:

                #adds card to decklists
                if revealed[3] in decklists[revealed[0]]:
                    decklists[revealed[0]][revealed[3]] += 1
                else:
                    decklists[revealed[0]].update({revealed[3]:1})


        return decklists




    def getOnPlay(self, game):
        # Who is on the play in this game?
        # Returns 'player' or 'opponent'
        onPlay = re.compile('(\S+) chooses to play first').search(' '.join(game[0])).group(1)
        return self.players[self.players.index(onPlay)]




    def getStartingHands(self, game):

        #format [(player1, cards), (player2, cards)]
        regex = re.compile(f'({self.players[0]}|{self.players[1]}) begins the game with (\w+) cards in hand | ({self.players[0]}|{self.players[1]}) puts.+on the bottom of their library and begins the game with (\w+) cards in hand')
        startingHands = re.findall(regex, ' '.join(game[0]))
        startingHands = [tuple(b for b in i if len(b) > 1) for i in startingHands]
        return startingHands




    def getWinner(self, game):

        #determines the winner or loser
        concededPattern = re.compile('(\S+) has conceded')
        winsPattern = re.compile('(\S+) wins the game')
        losesPattern = re.compile('(\S+) loses the game')

        conceded = concededPattern.search(' '.join([' '.join(i) for i in game]))
        wins = winsPattern.search(' '.join([' '.join(i) for i in game]))
        loses = losesPattern.search(' '.join([' '.join(i) for i in game]))

        if wins:
            return self.players[self.players.index(wins.group(1))][0]
        elif conceded:
            return [i for i in self.players if i not in self.players[self.players.index(conceded.group(1))]][0]
        elif loses:
            return self.players[self.players.index(loses.group(1))][0]
        else:
            return 'NA'
