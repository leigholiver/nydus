import os
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from support.Config import Config

class UsernamesDialog(QtWidgets.QDialog):
    def __init__(self, parent, config, base_path):
        super(UsernamesDialog, self).__init__(parent)
        uic.loadUi(base_path + '/lib/UsernamesDialog.ui', self)
        self.parent = parent
        config = Config()

        self.addUsernameButton.clicked.connect(self.addUsernameButtonPressed)
        self.username.returnPressed.connect(self.addUsernameButtonPressed)
        self.removeUsernameButton.clicked.connect(self.removeUsernameButtonPressed)

        for name in config.usernames:
            self.usernamesList.addItem(name)
        for name in config.recentUsernames:
            self.recentUsernamesList.addItem(name)
        self.recentUsernamesList.currentItemChanged.connect(self.recentUsernameSelected)

    def recentUsernameSelected(self, item):
        self.username.setText(item.text())

    def closeEvent(self, event):
        config = Config()
        config.usernames = []
        for name in self.usernamesList.findItems("*", Qt.MatchWildcard):
            if name.text() not in config.usernames:
                config.usernames.append(name.text())
            if name.text() in config.recentUsernames:
                config.recentUsernames.remove(name.text())

        if len(config.usernames) == 0:
            self.parent.usernamesLabel.show()
        else:
            self.parent.usernamesLabel.hide()

    def addUsernameButtonPressed(self):
        if self.username.text().strip() != "":
            self.usernamesList.addItem(self.username.text())
            for name in self.recentUsernamesList.findItems(self.username.text(), Qt.MatchWildcard):
                self.recentUsernamesList.takeItem(self.recentUsernamesList.row(name))
            self.username.clear()

    def removeUsernameButtonPressed(self):
        items = self.usernamesList.selectedItems()
        if not items: return
        for item in items:
            self.usernamesList.takeItem(self.usernamesList.row(item))
