import json, os
from PyQt5.QtCore import QObject, pyqtSignal
from .NydusBetConfig import NydusBetConfig


class Game(QObject):
    gameStarted = pyqtSignal(dict)
    gameEnded = pyqtSignal(str, list)

    def __init__(self, parent):
        QObject.__init__(self)
        self.parent = parent
        self.config = NydusBetConfig()
        self.game = None
        self.scores = self.config.scores
        self.escrow = {}

    def gameToDataFileDump(self):
        playerAName = playerBName = playerARace = playerBRace = ""
        playerAScore = playerBScore = 0
        
        if self.game:
            playerARace = self.game['playerARace']
            playerBRace = self.game['playerBRace']

            playerAName = self.game['playerA'] if self.config.myName == "" else self.config.myName
            if self.game['mode'] == 'caster':
                playerAName = self.game['playerA'] if self.config.playerAName == "" else self.config.playerAName
            playerBName = self.game['playerB'] if self.config.playerBName == "" else self.config.playerBName
            
            bets = {self.game['playerA']: 0, self.game['playerB']: 0 }
            for bet in self.game['bets']:
                bets[bet['player']] += bet['amount']
            
            playerAScore = int(bets[self.game['playerA']])
            playerBScore = int(bets[self.game['playerB']])


        with open(os.path.dirname(__file__) + "/display/js/data.js", 'w+') as outfile:
            outfile.write("window.data = " + json.dumps({
                'playerA': playerAName,
                'playerARace': playerARace,
                'playerAScore': playerAScore,
                'playerAColour': self.config.playerAColour,
                'playerB': playerBName,
                'playerBRace': playerBRace,
                'playerBScore': playerBScore,
                'playerBColour': self.config.playerBColour
            }))
            
    def startGame(self, data):
        if self.game != None and self.game['state'] != "ended":
            self.refundBets() # no scamreaper here
            
        self.game = self.gameFromData(data)
        if self.game != None:
            self.gameStarted.emit(self.game)
            self.gameToDataFileDump()

    def endGame(self, data):
        if self.game != None:
            self.setWinner(data)
            winnings = self.calculateWinnings()
                
            for w in winnings:
                if w['user'] in self.scores.keys():
                    self.scores[w['user']] += w['amount']
                else:
                    self.scores[w['user']] = w['amount']

            self.parent.log("Game ended - Winner: " + self.game['winner'] + ", Winnings: " + json.dumps(winnings))
            self.gameEnded.emit(self.game['winner'], winnings)
            self.game['state'] = "ended"
            self.escrow = {}
            self.config.scores = self.scores
            self.config.save()
            self.gameToDataFileDump()

    def close(self):
        if self.game != None:
            self.parent.log("Game closed")
            self.game['state'] = "closed"

    def setWinner(self, data):
        if self.game != None:
            for player in data['players']:
                if player['result'] == 'Victory':
                    self.game['winner'] = player['name']

    def calculateWinnings(self):
        winners = []
        if self.game != None:
            total = winTotal = 0
            winningBets = {}

            for bet in self.game['bets']:
                total += bet['amount']
                if bet['player'] == self.game['winner']:
                    winTotal += bet['amount']
                    if bet['user'] in winningBets.keys():
                        winningBets[bet['user']] += bet['amount']
                    else:
                        winningBets[bet['user']] = bet['amount']
            
            for winner in winningBets.keys():
                # distribute the total points between winners
                multiplier = winningBets[winner] / winTotal
                winnings = int(total * multiplier)

                # prize multiplier based on odds ie
                # 70% of bets win, pays out 1.3x your winnings
                # 30% of bets win, pays out 1.7x your winnings
                odds = winTotal/total
                winnings = int(winnings * (2 - odds))

                winners.append({ 'user': winner, 'amount': winnings })

        return winners

    def recordBet(self, user, player, amount):
        if self.game != None and self.game['state'] == 'open':
            betAmount = 0
            if user in self.scores.keys():
                if self.scores[user] > 0:
                    if self.scores[user] > amount:
                        betAmount = amount      
                    else:
                        betAmount = self.scores[user]

            if betAmount > 0:
                self.scores[user] -= betAmount
                if user in self.escrow.keys():
                    self.escrow[user] += betAmount
                else: 
                    self.escrow[user] = betAmount
            
            betAmount = 25 if betAmount <= 0 else betAmount + 25
            self.game['bets'].append({ 'user': user, 'player': player, 'amount': betAmount })
            self.parent.log("Bet recieved - " + json.dumps({ 'user': user, 'player': player, 'amount': betAmount }))
            self.gameToDataFileDump()

    def closeBets(self):
        if self.game != None:
            self.game['state'] = 'closed'

    def refundBets(self):
        self.parent.log("Refunding Bets")
        for user in self.escrow.keys():
            if user in self.scores.keys():
                self.scores[user] += self.escrow[user]
            else:
                self.scores[user] = self.escrow[user]
        self.escrow = {}

    def gameFromData(self, data):
        if len(data['players']) == 2:
            me = opponent = ""
            for player in data['players']:
                if player['isme']:
                    me = player['name']
                    race = player['race']
                else:
                    opponent = player['name']
                    oprace = player['race']
            if me != "" and opponent != "":
                return self.getGame('streamer', me, race, opponent, oprace)
            elif me == "":
                return self.getGame('caster', 
                    data['players'][0]['name'], 
                    data['players'][0]['race'], 
                    data['players'][1]['name'], 
                    data['players'][1]['race'])
            # else 
                # we are both players and cant really do anything
        return None

    def getGame(self, mode, playerA, playerARace, playerB, playerBRace):
        return {
            'mode': mode,
            'state': 'open',
            'winner': "",
            'playerA': playerA,
            'playerARace': playerARace,
            'playerB': playerB,
            'playerBRace': playerBRace,
            'bets': []
        }