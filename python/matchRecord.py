import re

class MatchRecord:

    def __init__(self, player):
        #sets self.player to player (will be none if player name isn't known)
        self.player = player



    def getDecklists(self, filename):
        decklists = []
        turn0 = dict()


        #gets matchLog
        with open(filename, 'rb') as f:
            #unknown characters are replaced by \ufffd (those question marks)
            self.matchLog = f.read().decode(encoding='utf-8', errors='replace')
        

        #tries to create self.players
        try:
            self.getPlayers()
            #if there is a problem reading the player names or the match is not 1v1 (fie invalid)
        except (IndexError, ValueError):
            return None


        #formats self.matchLog
        self.formatLines()


        #if there are less than 2 games, it's not a complete match
        if len(self.matchLog) < 2:
            return None
        

        #loops through each game
        for game in self.matchLog:
            
            #gets decklists of game
            gameDecklists = self.getDeckLists(game)
            if decklists is None:
                return None
            decklists.append(gameDecklists)


            #reformat
            try:
                turn0['play'] = self.getOnPlay(game)
            except:
                turn0['play'] = 'unknown'
            
            try:
                turn0['startingHands'] = self.getStartingHands(game)
            except:
                turn0['startingHands'] = 'unknown'
            
            winner = self.getWinner(game)

        
        return decklists            




    def getPlayers(self):
        #finds all players
        players = re.compile('@P(\S+) rolled').findall(self.matchLog)
        
        #if the player hasn't given their name, then name randomised
        if self.player is None:
            self.player, opponent = list(players)
        else:
            players.discard(self.player)
            opponent = list(players)[0]
        
        self.players = [self.player, opponent]
        del self.player




    def getDeckLists(self, game):
        decklists = {self.players[0]: tuple(), self.players[1]: tuple()}

        #stores cards each player has played, revealed, discarded, cycled
        #game actions are formatted as @P(player_name) (casts|plays|discards|cycles|reveals)
        #card names are formatted as @[Card Name@:numbers,numbers:@]
        playCardPattern = re.compile(f'({self.players[0]}|{self.players[1]}) (casts|plays|discards|cycles) (@\[([a-zA-Z\s,-]+)@:[0-9,]+:@\])')
        revealedCardPattern = re.compile(f'({self.players[0]}|{self.players[1]}) (reveals) (@\[([a-zA-Z\s,-]+)@:[0-9,]+:@\])')


        #finds matched patterns
        playCardMatches = playCardPattern.findall(' '.join(game))
        revealedMatches = revealedCardPattern.findall(' '.join(game))


        #if there are no taken game actions, exit
        if not playCardMatches:
            return None


        for actions in playCardMatches:

            #if a card has been revealed, and has interacted with the game, remove it from revealedMatches
            if actions[3] in revealedMatches:
                revealedMatches.pop(revealedMatches.index(actions[3]))

            decklists[actions[0]] += ((actions[3]),)


        for revealed in revealedMatches:
            decklists[revealed[0]] += ((revealed[3]),)


        return decklists



    def formatLines(self):
        #removes non-relevant characters
        filteredMatch = re.split(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff\ufffd\.\{\}\|\\=#\^><$]',self.matchLog)
        filteredMatch = [re.sub('^.*@P', '', line) for line in filteredMatch]
        filteredMatch = re.sub(re.compile('@\[([a-zA-Z\s,\'-]+)@:[0-9,]+:@\]'), r"\g<1>", ' '.join(filteredMatch))

        #splits games int format: [[gameAction1, gameAction2], [gameAction1], etc.]
        filteredMatch = re.split('chooses to play (foo|bar|baz)', ' '.join([line for line in filteredMatch if len(line) > 3]))
        self.matchLog = filteredMatch




    def getOnPlay(self, game):
        # Who is on the play in this game?
        # Returns 'player' or 'opponent'
        on_play = re.compile('(\S+) chooses to play first').search(game[0]).group(1)
        return self.players[self.players.index(on_play)]



    def getStartingHands(self, game):
        # Returns a dict containing the number of
        # cards in each player's starting hand
        # at a given game
        numDict = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7}

        starting_hands = [(self.players[self.players.index(match_obj.group(1).split()[0])], match_obj.group(2)) for match_obj in [re.compile('(.+) begins the game with (\w+) cards').search(line) for line in game] if match_obj]

        starting_hands = dict(starting_hands)
        for k, v in starting_hands.items():
            starting_hands[k] = numDict[v]

        return starting_hands



    def getWinner(self, game):

        #determines the winner or loser
        conceded_pattern = re.compile('(\S+) has conceded')
        wins_pattern = re.compile('(\S+) wins the game')
        loses_pattern = re.compile('(\S+) loses the game')

        conceded = conceded_pattern.search(' '.join(game))
        wins = wins_pattern.search(' '.join(game))
        loses = loses_pattern.search(' '.join(game))

        if wins:
            return (self.players[self.players.index(wins.group(1))], 'won')
        elif conceded:
            return ([i for i in self.players if i not in self.players[self.players.index(conceded.group(1))]], 'conceded')
        elif loses:
            return (self.players[self.players.index(loses.group(1))], 'loses')
        else:
            return 'NA'
