import os
from PyQt5 import QtWidgets, uic

class WebhookURLWindow(QtWidgets.QDialog):
    data = None

    def __init__(self, url):
        super(WebhookURLWindow, self).__init__()
        uic.loadUi(os.path.dirname(__file__) + '/WebhookURL.ui', self)

        self.enabledCheckbox.setChecked(url.data['enabled'])
        self.nameInput.setText(url.data['name'])
        self.urlInput.setText(url.data['url'])
        self.methodGet.setChecked(url.data['method'] == "GET")
        self.methodPost.setChecked(url.data['method'] == "POST")

        self.exec()

    def accept(self):
        self.data = {
            "name": self.nameInput.text(),
            "url": self.urlInput.text(),
            "enabled": self.enabledCheckbox.isChecked(),
            "method": "GET" if self.methodGet.isChecked() else "POST"
        }
        self.done(0)