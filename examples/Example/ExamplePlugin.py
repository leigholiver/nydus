
import sys, os, json
from PyQt5 import QtWidgets, uic
from support.plugins.NydusPlugin import NydusPlugin 

class ExampleWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ExampleWindow, self).__init__()
        uic.loadUi(os.path.dirname(__file__) + '/Example.ui', self)
        
class Example(NydusPlugin):
	name = "Example Plugin (Window)"
	info = "Example plugin to print events to a window"		
	website = "https://github.com/leigholiver/nydus"
		
	def __init__(self):
		NydusPlugin.__init__(self)
		self.ui = ExampleWindow()

	def getUI(self):
		self.ui.show()

	def enterGame(self, data):
		self.ui.label.setText("Enter game!\n" + json.dumps(data, indent=4, sort_keys=True))

	def exitGame(self, data):
		self.ui.label.setText("Exit game!\n" + json.dumps(data, indent=4, sort_keys=True))

	def menuChanged(self, data):
		self.ui.label.setText("Menu changed!\n" + json.dumps(data, indent=4, sort_keys=True))