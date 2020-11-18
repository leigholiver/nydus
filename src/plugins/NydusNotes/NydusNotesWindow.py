import os, json, re
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QSize, QPoint
from PyQt5.QtGui import QFont

_VERSION = 0.1
class NydusNotesWindow(QMainWindow):
    parent = None
    notes = {}
    recents = []
    loading = True
    op = None
    editing = None
    config_fontsize = 11

    def __init__(self, parent):
        super(NydusNotesWindow, self).__init__()
        uic.loadUi(os.path.dirname(__file__) + '/NydusNotes.ui', self)
        self.parent = parent
        self.setupUi()
        
        try:
            with open(os.path.dirname(__file__) + '/notes.json') as json_file:
                self.notes = json.load(json_file)
        except Exception as e:
            pass

    def startGame(self, opponent):
        self.searchResults.hide()
        self.op = opponent['name'] + "/" + opponent['race']
        self.loadNote(opponent['name'] + "/" + opponent['race'])
        self.statusLabel.setText("In game against " + opponent['name'] + "(" + opponent['race'] + ")")
        self.setMatchHistory(opponent['name'])

    def setMatchHistory(self, name):
        matches = self.parent.getMatchesForUser(name)
        self.matchHistory.clear()
        total = wins = winrate = 0
        for i in reversed(range(len(matches))):
            self.matchHistory.addItem(self.matchText(matches[i]))
            total += 1
            if matches[i]['result'] == "Victory":
                wins += 1
        if total > 0:
            winrate = int((wins/total) * 100)
            self.winrateLabel.setText("Match History - W: " + str(wins) + " L: " + str(total - wins) + " (" + str(winrate) + "%)")
            return
        self.winrateLabel.setText("Match History")
    
    def opponentSearch(self, query, results):
        results = []
        for key in self.notes.keys():
            if query.lower() in key.lower() and key not in results:
                results.append(key)
            if query.lower() in self.notes[key].lower() and key not in results:
                results.append(key)
        return results

    def addGame(self, match):
        self.recents.append(match)
        if len(self.recents) > 20:
            self.recents.pop(0)
        self.recentMatches.insertItem(0, self.matchText(match))
        self.statusLabel.setText(match['result'] + " against " + match['opponent'] + "(" + match['race'] + ")")
        self.setMatchHistory(match['opponent'])


    def getNotesFor(self, name, race):
        if name + "/" + race in self.notes.keys():
            return self.notes[name + "/" + race]
        elif name in self.notes.keys():
            return self.notes[name]
        return ""

    def loadNote(self, name):
        self.saveNote()
        if name != None:
            self.editing = name
            name = name.split("/")
            if len(name) == 1:
                name.append("")
            self.noteText.setText(self.getNotesFor(name[0], name[1]))
            self.setMatchHistory(name[0])

    def saveNote(self):
        if self.editing != None:
            self.notes[self.editing] = self.noteText.toPlainText()
            try:
                with open(os.path.dirname(__file__) + '/notes.json', 'w+') as outfile:
                    json.dump(self.notes, outfile, indent=4, sort_keys=True)
            except Exception as e:
                self.parent.log("Error saving notes file - " + str(e))
    
    def recentSelected(self, item):
        name = self.noteNameFromMatchText(item.text())
        self.parent.log(name)
        if name:
            self.loadNote(name)
        self.searchCancel.show()

    def searchResultSelected(self, item):
        self.loadNote(item.text())

    def searchButtonClicked(self):
        self.searchResults.clear()
        term = self.searchTerm.text()
        results = self.opponentSearch(term, [])
        for result in results:
            self.searchResults.addItem(result)
        self.searchResults.show()
        self.searchCancel.show()
    
    def searchCancelClicked(self):
        self.searchTerm.setText("")
        self.searchResults.clear()
        self.searchResults.hide()
        self.searchCancel.hide()
        self.loadNote(self.op)

    def matchText(self, match):
        return match['date'] + " - " + match['opponent'] + " (" + match['race'] + ") - " + match['result'] + " (" + self.gameTimeToTime(match['gametime']) + ")"

    def noteNameFromMatchText(self, matchText):
        x = re.split(" - (.*?) - ", matchText)
        if x:
            x = re.split(" \((.*?)\)", x[1])
            if x:
                return x[0] + "/" + x[1]
        return False

    def gameTimeToTime(self, gameTime):
        secs = float(gameTime)
        mins = secs / 60
        secs = secs % 60
        return str(int(mins)) + "m" + str(int(secs)) + "s"

    def setFontSize(self):
        font = QFont()
        font.setPointSize(self.fontSize.value())
        self.noteText.setFont(font)
        self.config_fontsize = self.fontSize.value()

    def setupUi(self):
        self.searchResults.hide()
        self.searchCancel.hide()
        self.searchButton.clicked.connect(self.searchButtonClicked)
        self.searchCancel.clicked.connect(self.searchCancelClicked)
        self.searchTerm.returnPressed.connect(self.searchButtonClicked)
        self.searchResults.itemClicked.connect(self.searchResultSelected)
        self.recentMatches.itemClicked.connect(self.recentSelected)
        self.adjustSize()
        
        try:
            with open(os.path.dirname(__file__) + '/config.json', 'r') as infile:
                cfg = json.load(infile)

                self.recents = cfg['recents']
                if cfg['size'] != None:
                    self.resize(QSize(cfg['size']['width'], cfg['size']['height']))
                if cfg['pos'] != None:
                    self.move(QPoint(cfg['pos']['x'], cfg['pos']['y']))
                self.fontSize.setValue(cfg['fontSize'])
        except Exception as e:
            pass
        
        for match in self.recents:
            self.recentMatches.insertItem(0, self.matchText(match))

        self.fontSize.valueChanged.connect(self.setFontSize)
        self.setFontSize()

    def closeEvent(self, event):
        self.saveNote()
        try:
            with open(os.path.dirname(__file__) + '/config.json', 'w+') as outfile:  
                json.dump({
                    'size': { "height": self.size().height(), "width": self.size().width() },
                    'pos': { "x": self.pos().x(), "y": self.pos().y() },
                    'fontSize': self.config_fontsize,
                    'recents': self.recents
                        
                }, outfile, indent=4, sort_keys=True)
        except Exception as e:
            self.parent.log("Error saving config file - " + str(e))