from support.plugins.NydusPlugin import NydusPlugin 
from .ScoreTrackerWindow import ScoreTrackerWindow

class ScoreTracker(NydusPlugin):
	name = "Score Tracker"
	info = "Automatically keep track of your scores vs each race and save these to a file"
	website = "https://github.com/leigholiver/nydus"
		
	def __init__(self):
		NydusPlugin.__init__(self)
		self.ui = ScoreTrackerWindow(self)

	def getUI(self):
		self.ui.show()

	def exitGame(self, data, isReplay):
		if not isReplay: self.ui.exitGame(data);