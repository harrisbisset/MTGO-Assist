import re
from collections import defaultdict
import os.path
from datetime import datetime
import sqlite3
from mtgtop8 import


class matchRecord:
    #TODO: find out what happens when a player mulls to zero.
    NUMS_DICT = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7}

    def __init__(self, filename, player=None):
        self.player = player
        with open(filename, 'rb') as f:
            self.match_log = f.read().decode(encoding='utf-8', errors='replace')
            #Unknown characters are replaced by \ufffd (those question marks)

        # Keep those line in this order

        #python mtg_scraper.py C:\Users\harri\AppData\Local\Apps\2.0\Data\JWMNX0QY.YK3\AGMD182G.AAW\mtgo..tion_92a8f782d852ef89_0003.0004_4d4c5524cb8c51a2\Data\AppFiles\E8BC386C00E942D40363482907EEDEEA
        
        self.records = defaultdict(dict)
        try:
            self.players = self._get_players()
        except (IndexError, ValueError):
            # There was a problem reading the player names
            # or the match is not 1v1
            self.records = None
            return
        
        # Record players as {'player': 'player_name', 'opponent': 'opp_name}
        #self.records['players'] = dict((v, k) for k, v in self.players.items())
        self._format_cards(filename)
        self._format_lines()
        self.games = self._get_games()
        if len(self.games) < 2:
            # If there are less than 2 games, it's not a complete match
            self.records = None
            return

        #self.players_wins = {'player': 0,'opponent': 0}

        date = datetime.fromtimestamp(os.path.getmtime(filename))
        turn0 = dict()
        for game in self.games:
            gameNum = self.games.index(game)+1
            turn0['play'] = self._get_on_play(game)
            turn0['startingHands'] = self._get_starting_hands(game)
            winner = self._get_winner(game)

            #run mtgtop8.py to get deckNames
            
            
            
            #insertgame into db

    def _get_players(self):

        # Find player names and set them as 'player' and 'opponent'.
        players = re.compile('@P(\S+) rolled').findall(self.match_log)

        if players is not None:
            self.player, self.opponent = list(players)
        else:
            players.discard(self.player)
            self.opponent = list(players)[0]

        return players

    def _format_cards(self):
        
        # Stores cards each player has played
        # The card names are formatted as @[Card Name@:numbers,numbers:@]
        #nums are maybe response time
        # Game actions are @P(player_name) (casts|plays|discards|cycles|reveals) card_pattern
        cardPattern = re.compile('@\[([a-zA-Z\s,\'-]+)@:[0-9,]+:@\]')
        revealedCardPattern = re.compile(f'@P({self.players[0]}|{self.players[1]}) (reveals) (@\[([a-zA-Z\s,-]+)@:[0-9,]+:@\])')
        playCardPattern = re.compile(f'@P({self.players[0]}|{self.players[1]}) (casts|plays|discards|cycles) (@\[([a-zA-Z\s,-]+)@:[0-9,]+:@\])')


        patternMatches = playCardPattern.findall(self.match_log)
        revealedMatches = revealedCardPattern.findall(self.match_log)
        self.knownCards = {f'{self.players[0]}': tuple(), f'{self.players[1]}': tuple()}


        for actions in patternMatches:

            #if card has been revealed, and has interacted with the game, remove it from revealedMatches
            if actions[3] in revealedMatches:
                revealedMatches.pop(revealedMatches.index(actions[3]))

            self.knownCards[actions[0]] = self.knownCards[actions[0]] + ((actions[3]),)
            
        for revealed in revealedMatches:
            self.knownCards[revealed[0]] = self.knownCards[revealed[0]] + ((revealed[3]),)


        # Replace the weird card formatting with a simple Card Name
        self.match_log = re.sub(cardPattern, r"\g<1>", self.match_log)

    def _format_lines(self):
        # Remove non-relevant characters
        filtered_match = re.split(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff\ufffd\.\{\}\|\\=#\^><$]',self.match_log)
        filtered_match = [re.sub('^.*@P', '', line) for line in filtered_match]
        filtered_match = [line for line in filtered_match if len(line) > 3]
        self.match_log = filtered_match

    # def _get_match_ID(self):
    #     # Match_ID looks like it's the first line of the filtered log.
    #     #not eventID


    #     return self.match_log[0]

    def _get_games(self):
        # Breakdown the match into different games.
        # Game 1 is games[0] and so on
        games = list()
        game_i = 0
        for i, line in enumerate(self.match_log):
            if "chooses to play" in line:
                games.append(self.match_log[game_i:i])
                game_i = i
        games.append(self.match_log[game_i:-1])
        games.pop(0)

        return games

    def _get_on_play(self, game):
        # Who is on the play in this game?
        # Returns 'player' or 'opponent'
        on_play = re.compile('(\S+) chooses to play first').search(game[0]).group(1)
        return self.players[self.players.index(on_play)]

    def _get_starting_hands(self, game):
        # Returns a dict containing the number of
        # cards in each player's starting hand
        # at a given game

        starting_hands = [(self.players[self.players.index(match_obj.group(1).split()[0])], match_obj.group(2)) for match_obj in [re.compile('(.+) begins the game with (\w+) cards').search(line) for line in game] if match_obj]

        starting_hands = dict(starting_hands)
        for k, v in starting_hands.items():
            starting_hands[k] = self.NUMS_DICT[v]

        return starting_hands

    def _get_winner(self, game):
        conceded_pattern = re.compile('(\S+) has conceded')
        wins_pattern = re.compile('(\S+) wins the game')
        loses_pattern = re.compile('(\S+) loses the game')

        conceded = conceded_pattern.search(' '.join(game))
        wins = wins_pattern.search(' '.join(game))
        loses = loses_pattern.search(' '.join(game))

        if wins:
            return (self.players[self.players.index(wins.group(1))], 'won')
        elif conceded:
            return ([i for i in self.players if i not in self.players[self.players.index(conceded.group(1))]])
        else:
            #manual input required
            pass
        # if wins:
        #     return (self.players[self.players.index(wins.group(1))], 'wins')
        # elif conceded:
        #     return (self.players[self.players.index(conceded.group(1))], 'conceded')
        # elif loses:
        #     return (self.players[self.players.index(loses.group(1))], 'loses')
        # else:
            # Sometimes players just leave the match
            # instead of properly conceding.
            # In those cases, query the user to check the game log
            
            #print('\n'.join(game[-8:]))
            # question = f"""Who won this game?
            # (1-{self.records['players']['player']})(2-{self.records['players']['opponent']})(3-draw)(4-unknown) """
            # answer = input(question).lower().strip()
            # print("")
            # while not(answer == "1" or answer == "2" or
            #         answer == "3" or answer == "4"):
            #     print("Please see valid answers.")
            #     answer = input(question).lower().strip()
            #     print("")
            # if answer[0] == "1":
            #     return 'player'
            # elif answer[0] == "2":
            #     return 'opponent'
            # elif answer[0] == "3":
            #     return 'draw'
            # else:
            #     return 'unknown'
            # return 'unknown'

    # def _get_last_turn(self, game):
    #     turn_pattern = re.compile('Turn (\d+)')
    #     # Iterating through finditer, only the last match is saved
    #     # This might save some memory
    #     for last_match in turn_pattern.finditer(' '.join(game)):
    #         pass

    #     return int(last_match.group(1))

    # def get_json(self):
    #     if not self.records:
    #         return None
    #     return json.dumps(self.records, default=str)
