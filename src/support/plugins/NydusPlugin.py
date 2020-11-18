from PyQt5.QtCore import QObject
from support.Logger import Logger

# The base object Nydus plugins must inherit from 
class NydusPlugin(QObject):
			
	# (string) The name of your plugin, to be displayed in the list
	name = ""
	
	# (string) Extended information about your plugin, displayed
	# when your plugin is selected in the plugin list
	info = ""

	# (string) You
	author = ""

	# (string) URL to display when your plugin is selected
	website = ""

	def __init__(self):
		QObject.__init__(self)
	
	# OPTIONAL
	# Run when the plugin is enabled, startup tasks 
	def start(self):
		pass

	# OPTIONAL
	# Run when the plugin is disabled, teardown tasks
	def stop(self):
		pass

	# OPTIONAL
	# (QMainWindow) Window to show when the Open Plugin button is clicked.
	def getUI(self):
		pass

	###################
	# Game state events 
	###################
	# (dict) data - the data of the current game 
	# data = {
	#   "players": [
	#     {
	#       "name": "playerA",
	#       "type": "user",
	#       "race": "Prot", # Terr | Zerg | Prot | random
	#       "result": "Defeat",
	#       "isme": "true"
	#     },
	#     {
	#       "name": "playerB",
	#       "type": "computer",
	#       "race": "random",
	#       "result": "Victory",
	#       "isme": "false"
	#     }
	#   ],
	#   "displayTime": "5.000000",
	#   "event": "enter" # enter | exit 
	# }
	# (bool) isReplay
	def enterGame(self, data, isReplay):
		pass

	def exitGame(self, data, isReplay):
		pass

	###################
	# Menu state events 
	###################
    # "ScreenScore/ScreenScore",
    # "ScreenUserProfile/ScreenUserProfile",
    # "ScreenBattleLobby/ScreenBattleLobby",
    # "ScreenHome/ScreenHome",
    # "ScreenSingle/ScreenSingle",
    # "ScreenCollection/ScreenCollection",
    # "ScreenCoopCampaign/ScreenCoopCampaign",
    # "ScreenCustom/ScreenCustom",
    # "ScreenReplay/ScreenReplay",
    # "ScreenMultiplayer/ScreenMultiplayer",
    # "ScreenLoading/ScreenLoading",
	def menuChanged(self, menu):
		pass

	###################
	# Debug Logging 
	###################
	# (string) message: message to add to the log
	def log(self, message):
		Logger().log("[" + self.name + "] " + message)