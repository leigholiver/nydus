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
                    self.log.emit("OBS Websocket connection error: [%s] %s " % (e.__class__.__name__, str(e)))
                except Exception as e:
                    self.log.emit("OBS Websocket error: [%s] %s " % (e.__class__.__name__, str(e)))
            time.sleep(1)
        if self.ws != None:
            self.ws.disconnect()
        
    def requestScenes(self):
        if not self.connected:
            return
            
        out = []
        try:
            scenes = self.ws.call(requests.GetSceneList())
            for s in scenes.getScenes():
                out.append(s['name'])
        except Exception as e:
            self.log.emit("OBS Websocket error getting scene list: [%s] %s " % (e.__class__.__name__, str(e)))

        self.sceneBroadcast.emit(out)

    def switchScene(self, scene):
        try:
            self.ws.call(requests.SetCurrentScene(scene))
        except Exception as e:
            self.log.emit("OBS websocket error switching scene: [%s] %s " % (e.__class__.__name__, str(e)))