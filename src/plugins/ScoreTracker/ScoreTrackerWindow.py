import os, json
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog

class ScoreTrackerWindow(QtWidgets.QMainWindow):
    def __init__(self, parent):
        super(ScoreTrackerWindow, self).__init__()
        uic.loadUi(os.path.dirname(__file__) + '/ScoreTracker.ui', self)
        self.parent = parent

        self.setupUi()
        self.scores = {
            'Terr': { 'Victory': 0, 'Defeat': 0 }, 
            'Prot': { 'Victory': 0, 'Defeat': 0 }, 
            'Zerg': { 'Victory': 0, 'Defeat': 0 } 
        }
        self.map = {
            'Terr': { 'Victory': self.terrWin, 'Defeat': self.terrLoss }, 
            'Prot': { 'Victory': self.protWin, 'Defeat': self.protLoss }, 
            'Zerg': { 'Victory': self.zergWin, 'Defeat': self.zergLoss } 
        }

        self.textTemplate.setText("vT: ${tw}-${tl}\nvZ: ${zw}-${zl}\nvP: ${pw}-${pl}")
        self.scoreFile = os.path.dirname(__file__) + '/scores.txt'

        try:
            with open(os.path.dirname(__file__) + '/scoretracker.json') as json_file:
                data = json.load(json_file)
                self.textTemplate.setText(data['template'])
                self.scoreFile = data['scoreFile']
        except Exception as e:
            self.parent.log("Error loading config file: " + str(e))

        self.setScoresFile.clicked.connect(self.openFileNameDialog)
        self.updateText()
        self.textTemplate.textChanged.connect(self.textChanged)
        self.scoresLabel.setText("Scores file location:\n" + os.path.abspath(self.scoreFile))

    def exitGame(self, data):
        if len(data['players']) == 2:
            race = ""
            result = ""
            for player in data['players']:
                if player['isme']:
                    if result != "":
                        self.parent.log("We are both players, Skipping game")
                        return
                    result = player['result']
                else:
                    race = player['race']
            if race != "" and result != "":
                if race == "random":
                        self.parent.log("Random player, skipping game")
                        return
                        
                self.scores[race][result] += 1
                self.updateScoreFields(race, result, self.scores[race][result])
                self.parent.log("Updating: " + race + "/" + result + ", now " + str(self.scores[race][result]))
                self.updateText()

    def updateScoreFields(self, race, result, value):
        self.map[race][result].setValue(value)

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "File to write scores to...", "","Text Files (*.txt)", options=options)
        if fileName:
            self.scoreFile = fileName
            self.save()
            self.scoresLabel.setText("Scores file location:\n" + os.path.abspath(self.scoreFile))

    def save(self):
        try:
            with open(os.path.dirname(__file__) + '/scoretracker.json', 'w+') as outfile:
                json.dump({
                    'template': self.textTemplate.toPlainText(),
                    'scoreFile': self.scoreFile
                }, outfile, indent=4, sort_keys=True)
        except Exception as e:
            self.parent.log("Error writing config file: " + str(e))

    def textChanged(self):
        self.save()
        self.updateText()

    def updateText(self):
        text = self.processText(self.textTemplate.toPlainText())
        self.preview.setText(text)
        try:
            with open(self.scoreFile, 'w+') as outfile:
                outfile.write(text)
        except Exception as e:
            self.parent.log("Error writing to score file: " + str(e))

    def processText(self, text):
        out = text.replace("${tw}", str(self.scores['Terr']['Victory']))
        out = out.replace("${tl}", str(self.scores['Terr']['Defeat']))
        out = out.replace("${zw}", str(self.scores['Zerg']['Victory']))
        out = out.replace("${zl}", str(self.scores['Zerg']['Defeat']))
        out = out.replace("${pw}", str(self.scores['Prot']['Victory']))
        out = out.replace("${pl}", str(self.scores['Prot']['Defeat']))
        return out

    def updateValue(self, race, result, value):
        self.scores[race][result] = value
        self.updateText()

    def incrementButtonPress(self, race, result):
        self.scores[race][result] += 1
        self.updateText()
    
    def decrementButtonPress(self, race, result):
        self.scores[race][result] -= 1
        self.updateText()

    def setupUi(self):
        self.terrWin.valueChanged.connect(lambda value: self.updateValue('Terr', 'Victory', value))
        self.terrLoss.valueChanged.connect(lambda value: self.updateValue('Terr', 'Defeat', value))
        self.zergWin.valueChanged.connect(lambda value: self.updateValue('Zerg', 'Victory', value))
        self.zergLoss.valueChanged.connect(lambda value: self.updateValue('Zerg', 'Defeat', value))
        self.protWin.valueChanged.connect(lambda value: self.updateValue('Prot', 'Victory', value))
        self.protLoss.valueChanged.connect(lambda value: self.updateValue('Prot', 'Defeat', value))