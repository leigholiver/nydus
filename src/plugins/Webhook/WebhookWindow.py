import os, json, requests
from urllib.parse import urlencode, quote
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from .WebhookURLListItem import WebhookURLListItem
from .WebhookURLWindow import WebhookURLWindow

class WebhookWindow(QtWidgets.QMainWindow):
    def __init__(self, parent):
        super(WebhookWindow, self).__init__()
        uic.loadUi(os.path.dirname(__file__) + '/Webhook.ui', self)
        self.parent = parent
        self.newButton.clicked.connect(self.newButtonPressed)
        self.editButton.clicked.connect(self.editButtonPressed)
        self.removeButton.clicked.connect(self.removeButtonPressed)

        try:
            with open(os.path.dirname(__file__) + '/data.json', 'r') as infile:  
                data = json.load(infile)
                for url in data:
                    self.urlList.addItem(WebhookURLListItem(url))
        except:
            pass

    def enterGame(self, data):
        data['event'] = 'enter'
        self.sendRequest(data)

    def exitGame(self, data):
        data['event'] = 'exit'
        self.sendRequest(data)

    def sendRequest(self, data):
        data = quote(json.dumps(data))
        if len(self.getAllItems()) == 0:
            print("No webhooks found, skipping event")
            return

        for item in self.getAllItems():
            if item.data['enabled']:
                url = item.data['url']
                if item.data['method'] == "GET":
                    delim = "?"
                    if url.find("?") != -1:
                        delim = "&"
                    url = url + delim + "json=" + data
                    try:
                        r = requests.get(url)
                        print("[" + item.data['name'] + "] GET " + str(r.status_code) + " (" + item.data['url'] + ")")
                    except Exception as e:
                        print("[" + item.data['name'] + "] GET " + str(e))
                else:
                    try:
                        r = requests.post(item.data['url'], data)
                        print("[" + item.data['name'] + "] POST " + str(r.status_code) + " (" + item.data['url'] + ")")
                    except Exception as e:
                        print("[" + item.data['name'] + "] POST " + str(e))

    def getAllItems(self):
        output = []
        for i in range(0,len(self.urlList)):
            output.append(self.urlList.item(i))
        return output

    def newButtonPressed(self):
        item = WebhookURLListItem({
            "name": "",
            "url": "",
            "enabled": False,
            "method": "GET",
        })
        result = WebhookURLWindow(item)
        if result.data != None:
            item.data = result.data
            item.updateText()
            self.urlList.addItem(item)
            self.save()

    def editButtonPressed(self):
        for item in self.urlList.selectedItems():
            result = WebhookURLWindow(item)
            if result.data != None:
                item.data = result.data
                item.updateText()
        self.save()

    def removeButtonPressed(self):
        items = self.urlList.selectedItems()
        if not items: return        
        for item in items:
            self.urlList.takeItem(self.urlList.row(item))
        self.save()

    def save(self):
        urls = []
        for item in self.getAllItems():
            urls.append(item.data)
        try:
            with open(os.path.dirname(__file__) + '/data.json', 'w') as outfile: 
                json.dump(urls, outfile, indent=4, sort_keys=True) 
        except Exception as e:
            print(e)