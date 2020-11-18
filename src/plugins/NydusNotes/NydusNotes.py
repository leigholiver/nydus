import os, json, datetime
from support.plugins.NydusPlugin import NydusPlugin 
from .NydusNotesWindow import NydusNotesWindow
        
class NydusNotes(NydusPlugin):
    name = "Nydus Notes"
    info = "Keep notes on your opponents and automatically display them when you enter a game (Huge thanks to Aggression1)"
    website = "https://github.com/leigholiver/nydus"

    matches = {}

    def __init__(self):
        NydusPlugin.__init__(self)
        try:
            with open(os.path.dirname(__file__) + '/matches.json') as json_file:
                self.matches = json.load(json_file)
        except Exception as e:
            pass
            
        self.ui = NydusNotesWindow(self)
    
    def getUI(self):
        self.ui.show()

    def enterGame(self, data, isReplay):
        if len(data['players']) == 2 and not isReplay:
            op = self.getOpponent(data)
            if not op:
                return
            self.ui.startGame(op)

    def exitGame(self, data, isReplay):
        if len(data['players']) == 2 and not isReplay:
            op = self.getOpponent(data)
            if not op:
                return
            self.ui.addGame(self.recordGame(data, op))

    def getMatchesForUser(self, user):
        if user in self.matches.keys():
            return self.matches[user];
        return []

    def recordGame(self, data, op):
        m = {
            'opponent': op['name'],
            'race': op['race'],
            'gametime': data['displayTime'],
            'result': self.myResultFromOP(op),
            'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        }

        if op['name'] in self.matches:
          self.matches[op['name']].append(m)
        else:
          self.matches[op['name']] = [ m ]

        try:
            with open(os.path.dirname(__file__) + '/matches.json', 'w+') as outfile:  
                json.dump(self.matches, outfile, indent=4, sort_keys=True)
        except Exception as e:
            self.log("Error saving matches file - " + str(e))
        return m


    def getOpponent(self, data):
        found = False
        op = {}

        for player in data['players']:
            if player['isme'] == True:
                if found:
                    # we are both players, just use
                    # this as opponent
                    op['name'] = player['name']
                    op['race'] = player['race']
                    op['result'] = player['result']
                found = True
            else:
                # just trust that we will be found, 
                # if this is p1 and we are p2 
                op['name'] = player['name']
                op['race'] = player['race']
                op['result'] = player['result']
        if not found:
            return False

        return op

    def myResultFromOP(self, op):
        if op['result'] == "Victory":
            return "Defeat"
        if op['result'] == "Defeat":
            return "Victory"
        return "Unknown"