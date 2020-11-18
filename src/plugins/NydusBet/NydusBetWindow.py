import os, json, re
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QIcon, QPixmap, QColor
from PyQt5.QtCore import pyqtSignal
from .NydusBetConfig import NydusBetConfig

class NydusBetWindow(QMainWindow):
    coloursUpdated = pyqtSignal()

    def __init__(self):
        super(NydusBetWindow, self).__init__()
        uic.loadUi(os.path.dirname(__file__) + '/NydusBet.ui', self)
        self.config = NydusBetConfig()
        self.setupUi()
        self.adjustSize()

    def closeEvent(self, event):
        self.config.save()

    def setupUi(self):
        self.username.setText(self.config.username)
        self.oauth.setText(self.config.oauth)
        self.channel.setText(self.config.channel)
        self.winText.setText(self.config.winText)
        self.loseText.setText(self.config.loseText)
        self.bettingOpenText.setText(self.config.bettingOpenText)
        self.casterModeBettingOpenText.setText(self.config.casterModeBettingOpenText)
        self.bettingClosedText.setText(self.config.bettingClosedText)
        self.bettingEndedText.setText(self.config.bettingEndedText)
        self.openTime.setValue(self.config.openTime)
        self.delay.setValue(self.config.delay)
        self.casterModeEnabled.setCheckState(self.config.casterModeEnabled)
        self.myName.setText(self.config.myName)
        self.playerAName.setText(self.config.playerAName)
        self.playerBName.setText(self.config.playerBName)

        self.username.textChanged.connect(lambda: setattr(self.config, 'username', self.username.text()))
        self.oauth.textChanged.connect(lambda: setattr(self.config, 'oauth', self.oauth.text()))
        self.channel.textChanged.connect(lambda: setattr(self.config, 'channel', self.channel.text()))
        self.winText.textChanged.connect(lambda: setattr(self.config, 'winText', self.winText.text()))
        self.loseText.textChanged.connect(lambda: setattr(self.config, 'loseText', self.loseText.text()))
        self.bettingOpenText.textChanged.connect(lambda: setattr(self.config, 'bettingOpenText', self.bettingOpenText.text()))
        self.casterModeBettingOpenText.textChanged.connect(lambda: setattr(self.config, 'casterModeBettingOpenText', self.casterModeBettingOpenText.text()))
        self.bettingClosedText.textChanged.connect(lambda: setattr(self.config, 'bettingClosedText', self.bettingClosedText.text()))
        self.bettingEndedText.textChanged.connect(lambda: setattr(self.config, 'bettingEndedText', self.bettingEndedText.text()))
        self.openTime.valueChanged.connect(lambda: setattr(self.config, 'openTime', self.openTime.text()))
        self.delay.valueChanged.connect(lambda: setattr(self.config, 'delay', self.delay.text()))
        self.casterModeEnabled.stateChanged.connect(lambda: setattr(self.config, 'casterModeEnabled', self.casterModeEnabled.checkState()))
        self.myName.textChanged.connect(lambda: setattr(self.config, 'myName', self.myName.text()))
        self.playerAName.textChanged.connect(lambda: setattr(self.config, 'playerAName', self.playerAName.text()))
        self.playerBName.textChanged.connect(lambda: setattr(self.config, 'playerBName', self.playerBName.text()))

        px = QPixmap(15,15);

        px.fill(QColor("#00ba00"))
        icon = QIcon(px)
        self.playerAColour.addItem(icon, "self")
        
        px.fill(QColor("#fe0000"))
        icon = QIcon(px)
        self.playerBColour.addItem(icon, "opponent")

        map = self.getColourMap()
        for label in map.keys():
            for combo in [self.playerAColour, self.playerBColour]:
                px.fill(QColor(map[label]))
                icon = QIcon(px)
                combo.addItem(icon, label)

        index = self.playerAColour.findText(self.config.playerAColour)
        if index >= 0:
            self.playerAColour.setCurrentIndex(index)
        
        index = self.playerBColour.findText(self.config.playerBColour)
        if index >= 0:
            self.playerBColour.setCurrentIndex(index)

        self.playerAColour.activated.connect(self.printcolor)
        self.playerBColour.activated.connect(self.printopcolor)
        
        self.browserSourceURL.setText(os.path.dirname(__file__) + "/display/index.html")

    def printcolor(self, index):
        self.config.playerAColour = self.playerAColour.currentText()
        self.coloursUpdated.emit()

    def printopcolor(self, index):
        self.config.playerBColour = self.playerBColour.currentText()
        self.coloursUpdated.emit()

    def getColourMap(self):
        return {
            'white': '#fefefe',
            'red': '#b3141e',
            'blue': '#0042fe',
            'teal': '#1ca6e9',
            'purple': '#540080',
            'yellow': '#eae029',
            'orange': '#fd890e',
            'green': '#167f00',
            'lightpink': '#cba5fb',
            'violet': '#1f01c8',
            'lightgrey': '#525493',
            'darkgreen': '#106246',
            'brown': '#4e2a04',
            'lightgreen': '#95fe90',
            'darkgrey': '#232323',
            'pink': '#e45baf',
        }