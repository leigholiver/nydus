from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow
from .F2ConfigWindow import F2ConfigWindow
from support.plugins.NydusPlugin import NydusPlugin 

class F2HabitBreaker(NydusPlugin):
    name = "F2HabitBreaker"
    info = "Create overlays to stop you clicking the all army button or the command card"        
    website = "https://github.com/leigholiver/nydus"
    
    def __init__(self):
        NydusPlugin.__init__(self)
        self.ui = F2ConfigWindow(self)
        self.windows = []

    def getUI(self):
        self.ui.show()

    def enterGame(self, data, isReplay):
        if not isReplay:
            windows = self.ui.windowsList.findItems("*", Qt.MatchWildcard)
            self.log("Entered game, showing " + str(len(windows)) + " windows")
            for window in windows:
                win = self.createWindow(window.data)
                self.windows.append(win)

    def exitGame(self, data, isReplay):
        if not isReplay:
            self.log("Entered game, hiding " + str(len(self.windows)) + " windows")
            for window in self.windows:
                window.close()

    def createWindow(self, data):
        win = QMainWindow()
        win.resize(data['size']['width'], data['size']['height'])
        win.move(data['pos']['x'], data['pos']['y'])
        win.setStyleSheet("QMainWindow { background-color: " + data['color'] + " }")
        # todo: fix opacity on linux
        win.setProperty("windowOpacity", data['opacity'])
        win.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        win.show()
        return win