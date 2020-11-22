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

    def stop(self):
        self.stopping = True
        if self.ws != None:
            self.ws.close()

    def run(self):
        while not self.stopping:
            if self.ws == None or self.connected == False:
                try:
                    self.ws = create_connection("ws://" + self.config.slobsIP + ":" + self.config.slobsPort + "/api/websocket",
                              sslopt={"cert_reqs": ssl.CERT_NONE, "check_hostname": False, "ssl_version": ssl.PROTOCOL_TLSv1})
                    self.doAuth()
                    self.connected = True
                    self.requestScenes()
                except Exception as e:
                    self.log.emit("Error connecting to Streamlabs OBS: [%s] %s" % (e.__class__.__name__, str(e)))
                    self.connected = False
            time.sleep(1)
        if self.ws != None:
            self.ws.close()
            self.connected = False
    
    def doAuth(self):
        self.ws.send(json.dumps({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "auth",
            "params": {
                "resource": "TcpServerService",
                "args": [self.config.slobsToken]
            }
        }))
        response =  self.ws.recv()
        response = json.loads(response)
        return response["result"] == True

    def requestScenes(self):
        if not self.connected:
            return

        out = []
        payload  = {
            "jsonrpc": "2.0",
            "id": 2,
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
                    print(response)
                    if isinstance(response["result"], list):
                        for scene in response["result"]:
                            scenes[scene["name"]] = scene["id"]
                            out.append(scene["name"])
                        self.scenes = scenes
                    else:
                        print("not a list tho %s" % str(response["result"]))
            except Exception as e:
                self.log.emit("Error parsing response from Streamlabs OBS: [%s] %s" % (e.__class__.__name__, str(e)))
                return
        self.sceneBroadcast.emit(out)

    def switchScene(self, scene):
        try:
            scene = self.scenes[scene]
        except Exception as e:
            self.log.emit("Could not find scene ID for " + scene + ", try refreshing scenes: [%s] %s" % (e.__class__.__name__, str(e)))
            return

        payload  = {
            "jsonrpc": "2.0",
            "id": 3,
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
                print(payload)
                self.ws.send(json.dumps(payload))
                response =  self.ws.recv()
                return response
            except Exception as e:
                self.log.emit("Error sending request to Streamlabs OBS: [%s] %s" % (e.__class__.__name__, str(e)))