import sys, json, requests, os, subprocess
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize, QPoint
from PyQt5.QtWidgets import QApplication
from ui.UsernamesDialog import UsernamesDialog
from ui.LogDialog import LogDialog
from support.Config import Config
from support.Logger import Logger

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, base_path, plugins):
        super(MainWindow, self).__init__()
        uic.loadUi(base_path + '/lib/nydus.ui', self)
        self.base_path = base_path

        self.plugins = plugins
        self.config = Config()
        self.logDialog = None
        self.usernamesDialog = None

        self.loading = True
        self.setupUI()
        self.loading = False

        self.adjustSize()
        self.show()

    def pluginSelected(self, item):
        if item != None:
            self.loading = True
            self.pluginInformation.setText(item.plugin.name + "\n" + item.plugin.info)
            self.pluginAuthor.setText(item.plugin.author)
            self.pluginWebsite.setText("<a href=\"" + item.plugin.website + "\">" + item.plugin.website + "</a>")
            if hasattr(item.plugin, 'getUI'):
                self.configurePlugin.setEnabled(True)
                self.showOnStartup.setEnabled(True)
            else:
                self.configurePlugin.setEnabled(False)
                self.showOnStartup.setEnabled(False)

            if self.config.plugins[item.id]["enabled"]:
                self.enablePlugin.setChecked(True)
            else:
                self.enablePlugin.setChecked(False)

            if self.config.plugins[item.id]["showOnStartup"]:
                self.showOnStartup.setChecked(True)
            else:
                self.showOnStartup.setChecked(False)
            self.loading = False


    def pluginDoubleClicked(self, item):
        if hasattr(item.plugin, 'getUI'):
            item.plugin.getUI()

    def toggleEnablePlugin(self):
        if not self.loading:
            item = self.pluginList.selectedItems()
            if item != []:
                self.togglePlugin(item[0], self.enablePlugin.isChecked())

    def pluginChecked(self, item):
        self.togglePlugin(item, item.checkState() == 2)

    def togglePlugin(self, item, checkState):
        if checkState:
            self.config.plugins[item.id]["enabled"] = True
            item.plugin.start()
            item.plugin.log("Enabled")
            item.setCheckState(Qt.Checked)
        else:
            self.config.plugins[item.id]["enabled"] = False
            item.plugin.stop()
            item.plugin.log("Disabled")
            item.setCheckState(Qt.Unchecked)
        self.refreshPluginPanel()

    def toggleShowOnStartup(self):
        if not self.loading:
            item = self.pluginList.selectedItems()
            if item != []:
                item = item[0]
                if self.showOnStartup.isChecked():
                    self.config.plugins[item.id]["showOnStartup"] = True
                    item.plugin.log("Show on startup enabled")
                else:
                    self.config.plugins[item.id]["showOnStartup"] = False
                    item.plugin.log("Show on startup disabled")

    def configurePluginPressed(self):
        item = self.pluginList.selectedItems()
        if item != []:
            item = item[0]
            if hasattr(item.plugin, 'getUI'):
                item.plugin.getUI()

    def startButtonPressed(self):
        if self.config.running:
            self.config.running = False
            self.startButton.setText("Start")
            self.statusLabel.setText("Nydus is stopped")
            Logger().log("[UI] Worker Stopped")
        else:
            self.config.running = True
            self.startButton.setText("Stop")
            self.statusLabel.setText("Nydus is running")
            Logger().log("[UI] Worker Started")

    def reloadPluginsPressed(self):
        self.plugins.reloadPlugins()
        self.setPluginList()

    def usernamesButtonPressed(self):
        if self.usernamesDialog == None:
            self.usernamesDialog = UsernamesDialog(self, self.config, self.base_path)
        self.usernamesDialog.show()

    def logButtonPressed(self):
        if self.logDialog == None:
            self.logDialog = LogDialog()
        self.logDialog.show()

    def pluginsFolderButtonPressed(self):
        self.openFile("plugins")

    def setPluginList(self):
        self.pluginList.clear()
        # self.plugins is the plugincollection, self.plugins.plugins
        # is the plugins contained in the plugincollection
        for plugin in self.plugins.plugins:
            if self.config.plugins[plugin.id]["enabled"]:
                plugin.setCheckState(Qt.Checked)
            else:
                plugin.setCheckState(Qt.Unchecked)

            self.pluginList.addItem(plugin)

        self.pluginList.sortItems()
        self.pluginList.setCurrentRow(0)
        self.refreshPluginPanel()

    def refreshPluginPanel(self):
        item = self.pluginList.selectedItems()
        if item != []:
            self.pluginSelected(item[0])

    def ipTextChanged(self, text):
        if not self.loading:
            self.config.ip = text

    def portTextChanged(self, text):
        if not self.loading:
            self.config.port = text

    def setupUI(self):
        self.pluginList.currentItemChanged.connect(self.pluginSelected)
        self.pluginList.itemDoubleClicked.connect(self.pluginDoubleClicked)
        self.pluginList.itemChanged.connect(self.pluginChecked)

        self.configurePlugin.clicked.connect(self.configurePluginPressed)
        self.reloadPlugins.clicked.connect(self.reloadPluginsPressed)
        self.pluginsFolderButton.clicked.connect(self.pluginsFolderButtonPressed)
        self.startButton.clicked.connect(self.startButtonPressed)
        self.logButton.clicked.connect(self.logButtonPressed)
        self.usernamesButton.clicked.connect(self.usernamesButtonPressed)
        if len(self.config.usernames) == 0:
            self.usernamesLabel.show()
        else:
            self.usernamesLabel.hide()

        self.pluginWebsite.setTextFormat(Qt.RichText)
        self.pluginWebsite.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.pluginWebsite.setOpenExternalLinks(True)

        self.updateLabel.setTextFormat(Qt.RichText)
        self.updateLabel.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.updateLabel.setOpenExternalLinks(True)
        self.updateLabel.hide()
        self.updateDescription.hide()

        self.enablePlugin.stateChanged.connect(self.toggleEnablePlugin)
        self.showOnStartup.stateChanged.connect(self.toggleShowOnStartup)

        self.ip.setText(self.config.ip)
        self.ip.textChanged.connect(self.ipTextChanged)
        self.port.setText(self.config.port)
        self.port.textChanged.connect(self.portTextChanged)

        if self.config.running:
            self.startButton.setText("Stop")
            self.statusLabel.setText("Nydus is running")
        else:
            self.startButton.setText("Start")
            self.statusLabel.setText("Nydus is stopped")

        self.setPluginList()
        self.adjustSize()

        if self.config.size != None:
            self.resize(QSize(self.config.size['width'], self.config.size['height']))
        if self.config.pos != None:
            self.move(QPoint(self.config.pos['x'], self.config.pos['y']))

    def updates(self, url, message):
            self.updateLabel.setText("<a href=\"" + url + "\">Update Available. Click here to download.</a>")
            self.updateDescription.setText(message)
            self.updateLabel.show()
            self.updateDescription.show()

    def closeEvent(self, event):
        self.config.size = { "height": self.size().height(), "width": self.size().width()}
        self.config.pos = { "x": self.pos().x(), "y": self.pos().y() }
        self.config.save()
        QApplication.quit()

    def openFile(self, filename):
        if sys.platform == "win32":
            os.startfile(filename)
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, filename])
