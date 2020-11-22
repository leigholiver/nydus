from PyQt5.QtWidgets import QListWidgetItem

class WebhookURLListItem(QListWidgetItem):
    def __init__(self, data):
        QListWidgetItem.__init__(self, "")
        self.data = data
        self.updateText()

    def updateText(self):
        self.setText(
             "[" + ("On" if self.data['enabled']  else "Off") + "] " + 
             self.data['name'] + 
             " (" + self.data['method'] + " " + self.data['url'] + ")"
        )