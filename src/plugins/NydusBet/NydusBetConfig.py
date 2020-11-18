import json, os

def NydusBetConfig():
    if _NydusBetConfig._instance is None:
        _NydusBetConfig._instance = _NydusBetConfig()
    return _NydusBetConfig._instance
    
class _NydusBetConfig:
    _instance = None

    def __init__(self):
        self.filename = os.path.dirname(__file__) + "/nydusbet.json"
        self.fromData({
            'username': "",
            'oauth': "", # www.twitchapps.com/tmi/
            'channel': "",
            'winText': 'Win', # bet command for win
            'loseText': 'Lose', # bet command for loss
            'bettingOpenText': "Game started against ${playerB} (${playerBRace}), use !Win or !Lose to bet!",
            'casterModeBettingOpenText': "${playerA} (${playerARace}) against ${playerB} (${playerBRace}), use !${playerA} or !${playerB} to bet!",
            'bettingClosedText': 'Betting Closed!',
            'bettingEndedText': '${winner} won!',
            'openTime': 300, # amount of time to leave bets open for 
            'delay': 0, # delay before sending chat messages
            'casterModeEnabled': 2, # fallback to caster mode if no usernames found
            'myName': '', # override my name
            'playerAName': "", # [caster mode] override player a name
            'playerBName': "", # [caster mode] override player b name
            'scores': {},
            'playerAColour': 'self',
            'playerBColour': 'opponent'
        })

        if os.path.exists(self.filename):
            try:
                self.load()
            except:
                pass

    def load(self):
        with open(self.filename) as json_file:
            data = json.load(json_file)
            self.fromData(data)

    def save(self):
        with open(self.filename, 'w+') as outfile:
            json.dump({
                'username': self.username,
                'oauth': self.oauth,
                'channel': self.channel,
                'winText': self.winText,
                'loseText': self.loseText,
                'bettingOpenText': self.bettingOpenText,
                'casterModeBettingOpenText': self.casterModeBettingOpenText,
                'bettingClosedText': self.bettingClosedText,
                'bettingEndedText': self.bettingEndedText,
                'openTime': self.openTime,
                'delay': self.delay,
                'casterModeEnabled': self.casterModeEnabled,
                'myName': self.myName,
                'playerAName': self.playerAName,
                'playerBName': self.playerBName,
                'scores': self.scores,
                'playerAColour': self.playerAColour,
                'playerBColour': self.playerBColour
            }, outfile, indent=4, sort_keys=True)

    def fromData(self, data):
        self.username = data['username']
        self.oauth = data['oauth']
        self.channel = data['channel']
        self.winText = data['winText']
        self.loseText = data['loseText']
        self.bettingOpenText = data['bettingOpenText']
        self.casterModeBettingOpenText = data['casterModeBettingOpenText']
        self.bettingClosedText = data['bettingClosedText']
        self.bettingEndedText = data['bettingEndedText']
        self.openTime = data['openTime']
        self.delay = data['delay']
        self.casterModeEnabled = data['casterModeEnabled']
        self.myName = data['myName']
        self.playerAName = data['playerAName']
        self.playerBName = data['playerBName']
        self.scores = data['scores']
        self.playerAColour = data['playerAColour']
        self.playerBColour = data['playerBColour']