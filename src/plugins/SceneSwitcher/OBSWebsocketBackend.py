import time
from obswebsocket import obsws, requests, exceptions
from PyQt5.QtCore import pyqtSignal
from .Backend import Backend
from .SceneSwitcherConfig import SceneSwitcherConfig

class OBSWebsocketBackend(Backend):

    def __init__(self):
        Backend.__init__(self)
        self.config = SceneSwitcherConfig()
        self.ws = obsws(self.config.websocketIP, self.config.websocketPort, self.config.websocketSecret)
        self.connected = False

    def run(self):
        while not self.stopping:
            if self.connected == False:
                try:
                    self.ws.connect()
                    self.connected = True
                    self.requestScenes()
                except exceptions.ConnectionFailure as e:
                    self.connected = False
                    self.log.emit("Error connecting to OBS Websocket - " + str(e))
                except Exception as e:
                    self.log.emit("Error in OBS Websocket - " + str(e))
            time.sleep(1)
        if self.ws != None:
            self.ws.disconnect()
        
    def requestScenes(self):
        out = []
        try:
            scenes = self.ws.call(requests.GetSceneList())
            for s in scenes.getScenes():
                out.append(s['name'])
        except Exception as e:
            self.log.emit("Error getting scene list from OBS Websocket - " + str(e))

        self.sceneBroadcast.emit(out)

    def switchScene(self, scene):
        try:
            self.ws.call(requests.SetCurrentScene(scene))
        except Exception as e:
            self.log.emit("Error switching scene - " + str(e))