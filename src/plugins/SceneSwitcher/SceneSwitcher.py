import sys, json, time
from PyQt5.QtCore import QTimer
from support.plugins.NydusPlugin import NydusPlugin 
from .SceneSwitcherWindow import SceneSwitcherWindow
from .SceneSwitcherConfig import SceneSwitcherConfig
from .SLOBSBackend import SLOBSBackend
from .OBSWebsocketBackend import OBSWebsocketBackend

CONFIG_SCENE_KEYS = [
    'sceneInGame',
    'sceneOutOfGame',
    'sceneReplay',
    'sceneObserving',
    'sceneLobby',
    'sceneScoreScreen',
    'sceneProfile',
    'sceneHome',
    'sceneCampaign',
    'sceneMultiplayer',
    'sceneReplaysMenu',
    'sceneCollection',
    'sceneCustom'
]

class SceneSwitcher(NydusPlugin):
    name = "Scene Switcher"
    info = "Switch scenes in OBS-Studio/Streamlabs OBS when you enter or leave a game or change menus (OBS-Studio requires the obs-websocket plugin)"
    website = "https://github.com/leigholiver/nydus"
        
    def __init__(self):
        NydusPlugin.__init__(self)
        self.ui = SceneSwitcherWindow(self)
        self.config = SceneSwitcherConfig()
        self.backend = None
        self.inGame = False
        self.menu = "ScreenHome/ScreenHome"
        self.scene = ""

    def getUI(self):
        self.requestScenes()
        self.ui.show()

    def start(self):
        self.backendSwitched(self.config.backend)

    def stop(self):
        try:
            if self.backend != None:
                self.backend.stop()
                self.backend = None
        except Exception as e:
            print("[%s] %s" % (e.__class__.__name__, str(e)))

    def enterGame(self, data, isReplay):
        self.inGame = True
        scene = ""

        if isReplay:
            scene = self.config.sceneReplay

        found = False
        for player in data['players']:
            if player['isme']:
                found = True

        if not found:
            scene = self.config.sceneObserving

        if scene != "" and scene != self.scene:
            self.switch(scene)
            return

        scene = self.config.sceneInGame
        if scene != "" and scene != self.scene:
            self.switch(scene)

    def exitGame(self, data, isReplay):
        # you might think we want to switch to the
        # out of game scene here, but we actually
        # want menuChanged to handle that
        self.inGame = False

    def menuChanged(self, data):
        if self.menu != data:
            self.menu = data
            if not self.inGame:
                if data == "ScreenLoading/ScreenLoading":
                    if self.config.switchOnLoading:
                        scene = self.config.sceneInGame
                        if scene != "" and scene != self.scene:
                            self.switch(scene)
                    # dont switch on loading screen
                    return


                scene = getattr(self.config, self.getSceneValue(data))
                if scene != "":
                    self.log("menu scene: " + scene)
                    if scene != self.scene:
                        self.switch(scene)
                    # we have a scene but we dont want to switch
                    # dont fall back to out of game scene
                    return
                
                scene = self.config.sceneOutOfGame
                if scene != "" and scene != self.scene:
                    self.switch(scene)

    def requestScenes(self):
        if self.backend != None:
            self.backend.requestScenes()

    def switch(self, scene):
        self.scene = scene
        self.log("Switching to " + scene)
        if self.backend != None:
            self.backend.switchScene(scene)

    def loadBackendScenes(self, backend):
        for key in CONFIG_SCENE_KEYS:
            if backend in self.config.backendScenes.keys() and key in self.config.backendScenes[backend].keys():
                setattr(self.config, key, self.config.backendScenes[backend][key])
            else:
                setattr(self.config, key, '')

    def saveBackendScenes(self, backend):
        out = {}
        for key in CONFIG_SCENE_KEYS:
            out[key] = getattr(self.config, key)
        self.config.backendScenes[backend] = out

    def backendSwitched(self, backend):
        if self.config.backend != backend:
            self.saveBackendScenes(self.config.backend)
            self.loadBackendScenes(backend)

        if self.backend != None:
            self.backend.stop()
            self.backend = None

        if backend == 'websocket':
            self.backend = OBSWebsocketBackend()
        elif backend == 'slobs':
            self.backend = SLOBSBackend()
        
        self.config.backend = backend
        if self.backend != None:
            self.backend.sceneBroadcast.connect(lambda scenes: self.ui.refreshScenes(scenes))
            self.backend.log.connect(lambda message: self.log(message))
            self.backend.start()

    def getSceneValue(self, key):
        data = {
            "ScreenScore/ScreenScore": "sceneScoreScreen",
            "ScreenUserProfile/ScreenUserProfile": "sceneProfile",
            "ScreenBattleLobby/ScreenBattleLobby": "sceneLobby",
            "ScreenHome/ScreenHome": "sceneHome",
            "ScreenSingle/ScreenSingle": "sceneCampaign",
            "ScreenCollection/ScreenCollection": "sceneCollection",
            "ScreenCoopCampaign/ScreenCoopCampaign": "sceneCampaign",
            "ScreenCustom/ScreenCustom": "sceneCustom",
            "ScreenReplay/ScreenReplay": "sceneReplaysMenu",
            "ScreenMultiplayer/ScreenMultiplayer": "sceneMultiplayer"
        }

        return data[key]