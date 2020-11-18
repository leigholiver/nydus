import sys, os
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QDialog,  QLabel, QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QKeySequence
from .SceneSwitcherConfig import SceneSwitcherConfig

class SceneSwitcherWindow(QtWidgets.QMainWindow):
    def __init__(self, parent):
        super(SceneSwitcherWindow, self).__init__()
        uic.loadUi(os.path.dirname(__file__) + '/SceneSwitcher.ui', self)
        self.parent = parent
        self.config = SceneSwitcherConfig()
        self.setupUi()
        self.adjustSize()
        self.loading = False

    def refreshScenes(self, scenes):
        self.loading = True
        comboMap = [
            { 'combo': self.inGameCombo, 'value': self.config.sceneInGame },
            { 'combo': self.outOfGameCombo, 'value': self.config.sceneOutOfGame },
            { 'combo': self.replayCombo, 'value': self.config.sceneReplay },
            { 'combo': self.observingCombo, 'value': self.config.sceneObserving },
            { 'combo': self.lobbyCombo, 'value': self.config.sceneLobby },
            { 'combo': self.scoreScreenCombo, 'value': self.config.sceneScoreScreen },
            { 'combo': self.profileCombo, 'value': self.config.sceneProfile },
            { 'combo': self.homeCombo, 'value': self.config.sceneHome },
            { 'combo': self.campaignCombo, 'value': self.config.sceneCampaign },
            { 'combo': self.multiplayerCombo, 'value': self.config.sceneMultiplayer },
            { 'combo': self.replaysMenuCombo, 'value': self.config.sceneReplaysMenu },
            { 'combo': self.collectionCombo, 'value': self.config.sceneCollection },
            { 'combo': self.customCombo, 'value': self.config.sceneCustom }
        ]

        for i in range(0, len(comboMap)):
            comboMap[i]['combo'].clear()
            comboMap[i]['combo'].addItem("")
            for scene in scenes:
                comboMap[i]['combo'].addItem(scene)

            index = comboMap[i]['combo'].findText(comboMap[i]['value'])
            if index >= 0:
                comboMap[i]['combo'].setCurrentIndex(index)
        self.loading = False

    def toggleBackend(self, backend, radio):
        if not self.loading and radio.isChecked():
            self.parent.backendSwitched(backend)

    def toggleSwitchOnLoadingScreen(self, state):
        if not self.loading:
            self.config.switchOnLoading = state
    
    def closeEvent(self, event):
        self.config.save()

    def setAttrIfNotLoading(self, obj, var, val):
        if not self.loading:
            setattr(obj, var, val)

    def setupUi(self):
        if self.config.backend == 'websocket': self.websocketRadio.setChecked(True)
        if self.config.backend == 'slobs': self.slobsRadio.setChecked(True)

        self.websocketIP.setText(self.config.websocketIP)
        self.websocketPort.setText(self.config.websocketPort)
        self.websocketSecret.setText(self.config.websocketSecret)
        self.slobsIP.setText(self.config.slobsIP)
        self.slobsPort.setText(self.config.slobsPort)
        self.switchOnLoading.setChecked(self.config.switchOnLoading)

        self.inGameCombo.currentTextChanged.connect(lambda value: self.setAttrIfNotLoading(self.config, 'sceneInGame', value))
        self.outOfGameCombo.currentTextChanged.connect(lambda value: self.setAttrIfNotLoading(self.config, 'sceneOutOfGame', value))
        self.replayCombo.currentTextChanged.connect(lambda value: self.setAttrIfNotLoading(self.config, 'sceneReplay', value))
        self.observingCombo.currentTextChanged.connect(lambda value: self.setAttrIfNotLoading(self.config, 'sceneObserving', value))
        self.lobbyCombo.currentTextChanged.connect(lambda value: self.setAttrIfNotLoading(self.config, 'sceneLobby', value))
        self.scoreScreenCombo.currentTextChanged.connect(lambda value: self.setAttrIfNotLoading(self.config, 'sceneScoreScreen', value))
        self.profileCombo.currentTextChanged.connect(lambda value: self.setAttrIfNotLoading(self.config, 'sceneProfile', value))
        self.homeCombo.currentTextChanged.connect(lambda value: self.setAttrIfNotLoading(self.config, 'sceneHome', value))
        self.campaignCombo.currentTextChanged.connect(lambda value: self.setAttrIfNotLoading(self.config, 'sceneCampaign', value))
        self.multiplayerCombo.currentTextChanged.connect(lambda value: self.setAttrIfNotLoading(self.config, 'sceneMultiplayer', value))
        self.replaysMenuCombo.currentTextChanged.connect(lambda value: self.setAttrIfNotLoading(self.config, 'sceneReplaysMenu', value))
        self.collectionCombo.currentTextChanged.connect(lambda value: self.setAttrIfNotLoading(self.config, 'sceneCollection', value))
        self.customCombo.currentTextChanged.connect(lambda value: self.setAttrIfNotLoading(self.config, 'sceneCustom', value))

        self.websocketIP.textChanged.connect(lambda: self.setAttrIfNotLoading(self.config, "websocketIP", self.websocketIP.text()))
        self.websocketPort.textChanged.connect(lambda: self.setAttrIfNotLoading(self.config, 'websocketPort', self.websocketPort.text()))
        self.websocketSecret.textChanged.connect(lambda: self.setAttrIfNotLoading(self.config, 'websocketSecret', self.websocketSecret.text()))
        self.slobsIP.textChanged.connect(lambda: self.setAttrIfNotLoading(self.config, 'slobsIP', self.slobsIP.text()))
        self.slobsPort.textChanged.connect(lambda: self.setAttrIfNotLoading(self.config, 'slobsPort', self.slobsPort.text()))

        self.slobsRadio.toggled.connect(lambda: self.toggleBackend('slobs', self.slobsRadio))
        self.websocketRadio.toggled.connect(lambda: self.toggleBackend('websocket', self.websocketRadio))
        self.connectButton.clicked.connect(lambda: self.parent.backendSwitched(self.config.backend))
        self.switchOnLoading.toggled.connect(lambda: self.toggleSwitchOnLoadingScreen(self.switchOnLoading.isChecked()))