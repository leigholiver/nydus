import json
from support.plugins.NydusPlugin import NydusPlugin

class ExampleNoGUI(NydusPlugin):
	# (string) The name of your plugin, to be displayed in the list
	name = "Example Plugin (Log)"

	# (string) Extended information about your plugin, displayed
	# when your plugin is selected in the plugin list
	info = "Example plugin to print events to the log"

	# (string) You
	author = ""

	# (string) URL to display when your plugin is selected
	website = "https://github.com/leigholiver/nydus"

	def __init__(self):
		NydusPlugin.__init__(self)

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
	def enterGame(self, data):
		self.log("Enter game! " + json.dumps(data))

	def exitGame(self, data):
		self.log("Exit game! " + json.dumps(data))

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
	def menuChanged(self, data):
		self.log("Menu changed!" + json.dumps(data))
