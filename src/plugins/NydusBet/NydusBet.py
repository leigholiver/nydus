import json
from PyQt5.QtCore import pyqtSignal, QTimer
from support.plugins.NydusPlugin import NydusPlugin
from support.Logger import Logger
from .Bot import Bot
from .Game import Game
from .NydusBetWindow import NydusBetWindow
from .NydusBetConfig import NydusBetConfig

class NydusBet(NydusPlugin):
    name = "Nydus Bet"
    info = "Automatic twitch chat betting on your games"
    website = "https://github.com/leigholiver/nydus"
    
    allowedChatFunctions = ['points', 'leaderboard']
    sendMessage = pyqtSignal(str)
    
    def __init__(self):
        NydusPlugin.__init__(self)
        self.config = NydusBetConfig()
        self.bot = None
        
        self.game = Game(self)
        self.game.gameStarted.connect(self.gameStarted)
        self.game.gameEnded.connect(self.gameEnded)

        self.ui = NydusBetWindow()
        self.ui.coloursUpdated.connect(lambda: self.game.gameToDataFileDump())

        self.currentGame = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.closeGame)
        self.timer.setSingleShot(True)

    def start(self):
        if not self.bot:
            self.bot = Bot(self, {
                'username': self.config.username,
                'oauth': self.config.oauth,
                'channel': self.config.channel
            })
            self.bot.start()
            self.bot.command.connect(self.command)
    
    def stop(self):
        if self.bot:
            self.bot.stop()
            self.bot = None

    # betting enter game
    def gameStarted(self, game):
        if game['mode'] == 'streamer':
            self.delaySendMessage(self.config.bettingOpenText)
        else:
            self.delaySendMessage(self.config.casterModeBettingOpenText)
        self.currentGame = game
        self.timer.start(self.config.openTime * 1000)

    # betting exit game 
    def gameEnded(self, winner, winners):
        messages = []
        for w in winners:
            messages.append(w['user'] + " (" + str(w['amount']) + ")")
        message = self.config.bettingEndedText
        if messages != []:
            message += " Winners: " + (", ".join(messages))
        self.delaySendMessage(message)

    def closeGame(self):
        self.game.close()
        message = self.config.bettingClosedText
        if len(self.currentGame['bets']) > 0:
            bets = { self.currentGame['playerA']: 0, self.currentGame['playerB']: 0 }
            for bet in self.currentGame['bets']:
                try:
                    bets[bet['player']] += bet['amount']
                except:
                    pass

            message += self.currentGame['playerA'] + ": " + str(bets[self.currentGame['playerA']]) + ", "
            message += self.currentGame['playerB'] + ": " + str(bets[self.currentGame['playerB']])

        self.delaySendMessage(message)

    def bet(self, user, player, params):
        amount = 0
        if len(params) > 0:
            try:
                amount = int(params[0])
            except:
                return
        self.game.recordBet(user, player, amount)

    # !points command
    def points(self, user, params):
        print(self.game.scores)
        score = escrow = 0
        if user in self.game.scores.keys():
            score = self.game.scores[user]
        if user in self.game.escrow.keys():
            escrow = self.game.escrow[user]
        message = user + ": " + str(score)
        if escrow > 0:
            message += " (~" + str(escrow) +")"
        self.sendMessage.emit(message)

    # !leaderboard command
    def leaderboard(self, user, params):
        leaders = []
        i = 0
        max = 4 if len(self.game.scores) > 4 else len(self.game.scores)
        for user, score in sorted(self.game.scores.items(), key=lambda item: item[1]):
            leaders.append(user + ": " + str(score))
            if i >= max:
                break
            i += 1
        if leaders != []:
            self.sendMessage.emit(", ".join(leaders))

    def injectText(self, text):
        if self.currentGame != None:
            if self.currentGame['mode'] == 'caster':
                playerAName = self.currentGame['playerA'] if self.config.playerAName == "" else self.config.playerAName
            else:
                playerAName = self.currentGame['playerA'] if self.config.myName == "" else self.config.myName
            
            playerBName = self.currentGame['playerB'] if self.config.playerBName == "" else self.config.playerBName
            winner = playerAName if self.currentGame['winner'] == self.currentGame['playerA'] else playerBName
            text = text.replace("${playerA}", playerAName)
            text = text.replace("${playerARace}", self.currentGame['playerARace'])
            text = text.replace("${playerB}", playerBName)
            text = text.replace("${playerBRace}", self.currentGame['playerBRace'])
            text = text.replace("${winner}", winner)
        return text
            
    def command(self, user, command, params):
        if command in self.allowedChatFunctions:
            try:
                getattr(self, command)(user, params)
                return
            except Exception as e:
                print(e)
        
        if self.currentGame != None:
            if self.currentGame['mode'] == 'caster':
                if command.lower() == self.currentGame['playerA'].lower() or command.lower() == self.config.playerAName.lower():
                    self.bet(user, self.currentGame['playerA'], params)
                if command.lower() == self.currentGame['playerB'].lower() or command.lower() == self.config.playerBName.lower():
                    self.bet(user, self.currentGame['playerB'], params)
            else:
                if command.lower() == self.config.winText.lower():
                    self.bet(user, self.currentGame['playerA'], params)
                elif command.lower() == self.config.loseText.lower():
                    self.bet(user, self.currentGame['playerB'], params)
    
    def delaySendMessage(self, message):
        QTimer.singleShot(self.config.delay * 1000, lambda: self.sendMessage.emit(self.injectText(message)))

    # plugin enter game
    def enterGame(self, data, isReplay):
        if not isReplay:
            self.game.startGame(data)

    # plugin exit game
    def exitGame(self, data, isReplay):
        if not isReplay:
            self.game.endGame(data)

    def getUI(self):
        self.ui.show()