import sys, os, json
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout, QPushButton, QFileDialog
from PyQt5.QtCore import Qt

class SoundOfVictoryWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(SoundOfVictoryWindow, self).__init__()
        uic.loadUi(os.path.dirname(__file__) + '/SoundOfVictory.ui', self)
        
        self.data = {
            'Victory': '',
            'Defeat': ''
        }

        try:
            with open(os.path.dirname(__file__) + '/data.json', 'r') as infile:  
                self.data = json.load(infile)
        except:
            pass 

        self.victoryLabel.setText(self.data['Victory'])
        self.victorySet.clicked.connect(lambda: self.openFileNameDialog('Victory'))
        self.victoryClear.clicked.connect(lambda: self.clear('Victory'))

        self.defeatLabel.setText(self.data['Defeat'])
        self.defeatSet.clicked.connect(lambda: self.openFileNameDialog('Defeat'))
        self.defeatClear.clicked.connect(lambda: self.clear('Defeat'))
        self.adjustSize()

    def clear(self, type):
        self.data[type] = ''
        self.save()
        if type == 'Victory': label = self.victoryLabel
        if type == 'Defeat': label = self.defeatLabel
        label.setText('')

    def openFileNameDialog(self, outcome):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*)", options=options)
        if fileName:
            self.data[outcome] = fileName
            if outcome == 'Defeat':
                self.defeatLabel.setText(fileName)
            else:
                self.victoryLabel.setText(fileName)
            self.save()
    
    def save(self):
        with open(os.path.dirname(__file__) + '/data.json', 'w') as outfile:  
            json.dump(self.data, outfile, indent=4, sort_keys=True)