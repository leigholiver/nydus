from PyQt5.QtWidgets import QListWidgetItem

class WindowListItem(QListWidgetItem):
    def __init__(self, data):
        QListWidgetItem.__init__(self, "")
        self.data = data
        self.updateText()

    def updateText(self):
        self.setText(
             "[" + self.data['name'] + "] " +
             "w: " + str(self.data['size']['width']) + " - " +
             "h: " + str(self.data['size']['height']) + " - " + 
             "x: " + str(self.data['pos']['x']) + " - " + 
             "y: " + str(self.data['pos']['y']) + " - " + 
             "color: " + str(self.data['color']) + " - " + 
             "opacity: " + str(self.data['opacity'])
        )