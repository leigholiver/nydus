from support.plugins.NydusPlugin import NydusPlugin 
from .WebhookWindow import WebhookWindow
        
class Webhook(NydusPlugin):
	name = "Webhook"
	info = "Send web requests containing game data when entering/leaving a game"		
	website = "https://github.com/leigholiver/nydus"
		
	def __init__(self):
		NydusPlugin.__init__(self)
		self.ui = WebhookWindow(self)

	def getUI(self):
		self.ui.show()

	def enterGame(self, data, isReplay):
		if not isReplay: self.ui.enterGame(data)

	def exitGame(self, data, isReplay):
		if not isReplay: self.ui.exitGame(data)