import requests, json, ssl, time
from websocket import create_connection
from .Backend import Backend
from .SceneSwitcherConfig import SceneSwitcherConfig

class SLOBSBackend(Backend):

    def __init__(self):
        Backend.__init__(self)
        self.config = SceneSwitcherConfig()
        self.scenes = {}
        self.ws = None
        self.connected = False

    def run(self):
        while not self.stopping:
            if self.ws == None or self.connected == False:
                try:
                    self.ws = create_connection("ws://" + self.config.slobsIP + ":" + self.config.slobsPort + "/api/websocket",
                              sslopt={"cert_reqs": ssl.CERT_NONE, "check_hostname": False, "ssl_version": ssl.PROTOCOL_TLSv1})
                    self.connected = True
                    self.requestScenes()
                except Exception as e:
                    self.log.emit("Error connecting to Streamlabs OBS - " + str(e))
                    self.connected = False
            time.sleep(1)
        if self.ws != None:
            self.ws.close()
        
    def requestScenes(self):
        out = []
        payload  = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getScenes",
            "params": {
                "resource": "ScenesService"
            }
        }
        response = self.request(payload)
        if response != None:
            try:
                response = json.loads(response)
                scenes = {}
                if response != None:
                    for scene in response["result"]:
                        scenes[scene["name"]] = scene["id"]
                        out.append(scene["name"])
                self.scenes = scenes
            except Exception as e:
                self.log.emit("Error parsing response from Streamlabs OBS - " + str(e))
        self.sceneBroadcast.emit(out)

    def switchScene(self, scene):
        try:
            scene = self.scenes[scene]
        except Exception as e:
            self.log.emit("Could not find scene ID for " + scene + ", try refreshing scenes - " + str(e))

        payload  = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "makeSceneActive",
            "params": {
                "resource": "ScenesService",
                "args": [ scene ]
            }
        }
        response = self.request(payload)

    def request(self, payload):
        if not self.connected:
            self.start()

        if self.connected:
            try:
                self.ws.send(json.dumps(payload))
                response =  self.ws.recv()
                return response
            except Exception as e:
                self.log.emit("Error sending request to Streamlabs OBS - " + str(e))