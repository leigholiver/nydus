import time
import obsws_python as obsws
from PyQt5.QtCore import pyqtSignal
from .Backend import Backend
from .SceneSwitcherConfig import SceneSwitcherConfig

class OBSWebsocketBackend(Backend):

    def __init__(self):
        Backend.__init__(self)
        self.config = SceneSwitcherConfig()
        self.ws = None

    def run(self):
        while not self.stopping:
            try:
                if self.ws == None:
                    self.ws = obsws.ReqClient(
                        host=self.config.websocketIP,
                        port=self.config.websocketPort,
                        password=self.config.websocketSecret
                    )
                else:
                    self.requestScenes()
            except Exception as e:
                self.log.emit("OBS Websocket error: [%s] %s " % (e.__class__.__name__, str(e)))
                self.ws = None

            if self.stopping:
                self.ws = None

            time.sleep(0.5)

    def requestScenes(self):
        try:
            resp = self.ws.get_scene_list()
            scenes = [di.get("sceneName") for di in reversed(resp.scenes)]
            self.sceneBroadcast.emit(scenes)
        except Exception as e:
            self.log.emit("OBS Websocket error getting scene list: [%s] %s " % (e.__class__.__name__, str(e)))
            raise e

    def switchScene(self, scene):
        try:
            self.ws.set_current_program_scene(scene)
        except Exception as e:
            self.log.emit("OBS websocket error switching scene: [%s] %s " % (e.__class__.__name__, str(e)))
            raise e
