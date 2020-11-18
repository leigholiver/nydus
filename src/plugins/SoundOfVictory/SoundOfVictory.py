import os, json
from playsound import playsound
from support.plugins.NydusPlugin import NydusPlugin 
from .SoundOfVictoryWindow import SoundOfVictoryWindow
        
class SoundOfVictory(NydusPlugin):
    name = "Sound of Victory"
    info = "Play a sound when you win or lose"
    website = "https://github.com/leigholiver/nydus"

    def __init__(self):
        NydusPlugin.__init__(self)
        self.ui = None

    def exitGame(self, data, isReplay):
        if not isReplay:
            for player in data['players']:
                if player['isme'] and (player['result'] == "Victory" or player['result'] == "Defeat"):
                    try:
                        with open(os.path.dirname(__file__) + '/data.json', 'r') as infile:
                            sounds = json.load(infile)
                            file = sounds[player['result']]
                            self.log("Playing file " + file)
                            try:
                                # try to play asynchronously if we can, so we 
                                # dont hold up all the other events until the 
                                # sound is done playing
                                playsound(file, False)
                            except Exception as e: 
                                self.log("Couldn't play sound asynchronously: " + str(e))
                                try:
                                    playsound(file)
                                except Exception as e:
                                    self.log("Couldn't play sound: " + str(e))
                                    pass
                    except Exception as e:
                        self.log("Error: " + str(e))
                    return

    def getUI(self):
        if self.ui == None:
            self.ui = SoundOfVictoryWindow()
        self.ui.show()