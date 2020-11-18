from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.Qt import Qt
from support.Config import Config

class PluginListItem(QListWidgetItem):
    def __init__(self, plugin, id):
        QListWidgetItem.__init__(self, plugin.name)
        self.id = id
        self.plugin = plugin
        self.setFlags(self.flags() | Qt.ItemIsUserCheckable)
        
    def getUI(self):
        return self.plugin.getUI()