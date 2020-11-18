from PyQt5.QtCore import QThread, pyqtSignal
from support.Logger import Logger

class Backend(QThread):
	sceneBroadcast = pyqtSignal(list)
	log = pyqtSignal(str)
	stopping = False

	def requestScenes(self): pass
	def switchScene(self, scene): pass

	def stop(self):
		self.stopping = True
