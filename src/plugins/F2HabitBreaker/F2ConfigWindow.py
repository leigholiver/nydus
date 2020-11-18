import os, json
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QPushButton, QColorDialog, QSlider, QLabel, QListWidget
from .WindowListItem import WindowListItem
from .WindowPlacementDialog import WindowPlacementDialog

class F2ConfigWindow(QMainWindow):
    def __init__(self, parent):
        super(F2ConfigWindow, self).__init__()
        uic.loadUi(os.path.dirname(__file__) + '/F2HabitBreaker.ui', self)
        self.loading = True
        self.parent = parent
        try:
            with open(os.path.dirname(__file__) + '/data.json', 'r') as infile:  
                windows = json.load(infile)
        except Exception as e:
            self.parent.log("Error opening configuration file - " + str(e))
            windows = self.defaultWindows()

        for window in windows:
            self.windowsList.addItem(WindowListItem(window))
            
        self.windowsList.currentItemChanged.connect(self.windowSelected)
        self.newWindow.clicked.connect(self.newWindowPressed)
        self.removeButton.clicked.connect(self.removeButtonPressed)
        self.colourButton.clicked.connect(self.selectColor)
        self.opacitySlider.valueChanged.connect(self.setOpacity)
        self.nameInput.textChanged.connect(self.nameInputChanged)
        self.adjustSize()

        self.loading = False
   
    def removeButtonPressed(self):
        items = self.windowsList.selectedItems()
        if not items: return        
        for item in items:
            self.windowsList.takeItem(self.windowsList.row(item))    
        self.save()
   
    def recordPosition(self, data):
        self.windowsList.addItem(WindowListItem(data))
        self.save()

    def selectColor(self):
        color = QColorDialog.getColor().name()
        self.colourLabel.setStyleSheet("background-color: " + color);
        items = self.windowsList.selectedItems()
        if not items: return        
        for item in items:
            item.data['color'] = color
            item.updateText()
        self.save()

    def nameInputChanged(self):
        if not self.loading:
            items = self.windowsList.selectedItems()
            if not items: return        
            for item in items:
                item.data['name'] = self.nameInput.text()
                item.updateText()
            self.save()

    def setOpacity(self):
        if not self.loading:
            opacity = self.opacitySlider.value() / 100
            items = self.windowsList.selectedItems()
            if not items: return        
            for item in items:
                item.data['opacity'] = opacity
                item.updateText()
            self.save()

    def newWindowPressed(self):
        WindowPlacementDialog(self)

    def windowSelected(self, item):
        if item != None:
            self.loading = True
            self.colourLabel.setStyleSheet("background-color: " + item.data['color']);
            self.opacitySlider.setValue(item.data['opacity'] * 100)
            self.nameInput.setText(item.data['name'])
            self.loading = False

    def save(self):
        try:
            with open(os.path.dirname(__file__) + '/data.json', 'w') as outfile:  
                windows = []
                for window in self.windowsList.findItems("*", Qt.MatchWildcard):
                    windows.append(window.data)
                json.dump(windows, outfile, indent=4, sort_keys=True)
        except Exception as e:
            self.parent.log("Error saving configuration file - " + str(e))

    def defaultWindows(self):
        return  [
            # F2 button
            {
                "name": "All Army Button",
                "color": "#000000",
                "opacity": 0.4,
                "pos": {
                    "x": 83,
                    "y": 757
                },
                "size": {
                    "height": 45,
                    "width": 72
                }
            },
            # Command Card
            {
                "name": "Command Card",
                "color": "#000000",
                "opacity": 0.4,
                "pos": {
                    "x": 1530,
                    "y": 840
                },
                "size": {
                    "height": 230,
                    "width": 370
                }
            }
        ]