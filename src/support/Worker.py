from PyQt5.QtCore import QThread, QTimer, pyqtSignal
from support.Config import Config
import requests, random, time
from support.Logger import Logger

class Worker(QThread):
    enterGame = pyqtSignal(dict, bool)
    exitGame = pyqtSignal(dict, bool)
    menuChanged = pyqtSignal(str)
    log = pyqtSignal(str)

    def __init__(self):
        super(Worker, self).__init__()
        self.inGame = False
        self.menu = ""

        self.initialTimeout = 0.5
        self.maxTimeout = 5

        self.timeout = self.initialTimeout

    def run(self):
        while True:
            config = Config()
            if config.running:
                URL = "http://" + config.ip + ":" + config.port;
                try:
                    r = requests.get(URL + "/ui")
                    if not r.status_code == 200:
                        raise Exception("No game response from " + URL)
                    uiResponse = r.json()
                    r = requests.get(URL + "/game")
                    if not r.status_code == 200:
                        raise Exception("No ui response from " + URL)
                    gameResponse = r.json()
                    self.timeout = self.initialTimeout
                    
                    try:
                        if (len(uiResponse['activeScreens']) == 0 
                            and not self.inGame 
                            and gameResponse['players'][0]['result'] == "Undecided"):
                            self.inGame = True
                            self.log.emit("[Worker] Enter game")
                            self.processResponse(gameResponse)
                            self.enterGame.emit(gameResponse, gameResponse['isReplay'] == "true")

                        if len(uiResponse['activeScreens']) > 0 and self.inGame:
                            self.inGame = False
                            self.log.emit("[Worker] Exit game")
                            self.processResponse(gameResponse)
                            self.exitGame.emit(gameResponse, gameResponse['isReplay'] == "true")

                        menu = self.getActiveMenuLabel(uiResponse)
                        if menu != self.menu and menu != "":
                            self.log.emit("[Worker] Menu changed to " + menu)
                            self.menuChanged.emit(menu)
                            self.menu = menu
                    except Exception as e:
                        self.log.emit("[Worker] " + str(e))
                        
                except Exception as e:
                    self.log.emit("[Worker] " + str(e))
                    self.timeout = self.maxTimeout
                    self.log.emit("[Worker] Trying again in %d seconds" % self.timeout)

            time.sleep(self.timeout)

    def getActiveMenuLabel(self, uiResponse):
        menus = [
            "ScreenScore/ScreenScore",
            "ScreenUserProfile/ScreenUserProfile",
            "ScreenBattleLobby/ScreenBattleLobby",
            "ScreenHome/ScreenHome",
            "ScreenSingle/ScreenSingle",
            "ScreenCollection/ScreenCollection",
            "ScreenCoopCampaign/ScreenCoopCampaign",
            "ScreenCustom/ScreenCustom",
            "ScreenReplay/ScreenReplay",
            "ScreenMultiplayer/ScreenMultiplayer",
            "ScreenLoading/ScreenLoading",
        ]

        for menu in menus:
            if menu in uiResponse['activeScreens']:
                return menu

        return ""

    def processResponse(self, gameResponse):
        self.updatePlayerIsMe(gameResponse)
        self.updateRecentUsernames(gameResponse)

    def updatePlayerIsMe(self, gameResponse):
        config = Config()
        for player in gameResponse['players']:
            player['isme'] = False
            if player['name'] in config.usernames:
                player['isme'] = True

    def updateRecentUsernames(self, gameResponse):
        config = Config()
        for player in gameResponse['players']:
            if player['name'] not in config.usernames and player['name'] not in config.recentUsernames:
                config.recentUsernames.append(player['name'])