import json, os

def SceneSwitcherConfig():
    if _SceneSwitcherConfig._instance is None:
        _SceneSwitcherConfig._instance = _SceneSwitcherConfig()
    return _SceneSwitcherConfig._instance
    
class _SceneSwitcherConfig:
    _instance = None

    def __init__(self):
        self.filename = os.path.dirname(__file__) + "/sceneswitcher.json"
        self.fromData({
            'backend': '',
            'websocketIP': 'localhost',
            'websocketPort': '4444',
            'websocketSecret': 'secret',
            'slobsIP': 'localhost',
            'slobsPort': '59650',
            'sceneInGame': '',
            'sceneOutOfGame': '',
            'sceneReplay': '',
            'sceneObserving': '',
            'sceneLobby': '',
            'sceneScoreScreen': '',
            'sceneProfile': '',
            'sceneHome': '',
            'sceneCampaign': '',
            'sceneMultiplayer': '',
            'sceneReplaysMenu': '',
            'sceneCollection': '',
            'sceneCustom': '',
            'switchOnLoading': False
        })

        if os.path.exists(self.filename):
            try:
                self.load()
            except:
                pass

    def load(self):
        with open(self.filename) as json_file:
            data = json.load(json_file)
            self.fromData(data)

    def save(self):
        with open(self.filename, 'w+') as outfile:
            json.dump({
                'backend': self.backend,
                'websocketIP': self.websocketIP,
                'websocketPort': self.websocketPort,
                'websocketSecret': self.websocketSecret,
                'slobsIP': self.slobsIP,
                'slobsPort': self.slobsPort,
                'sceneInGame': self.sceneInGame,
                'sceneOutOfGame': self.sceneOutOfGame,
                'sceneReplay': self.sceneReplay,
                'sceneObserving': self.sceneObserving,
                'sceneLobby': self.sceneLobby,
                'sceneScoreScreen': self.sceneScoreScreen,
                'sceneProfile': self.sceneProfile,
                'sceneHome': self.sceneHome,
                'sceneCampaign': self.sceneCampaign,
                'sceneMultiplayer': self.sceneMultiplayer,
                'sceneReplaysMenu': self.sceneReplaysMenu,
                'sceneCollection': self.sceneCollection,
                'sceneCustom': self.sceneCustom,
                'switchOnLoading': self.switchOnLoading
            }, outfile, indent=4, sort_keys=True)

    def fromData(self, data):
        self.backend = data['backend']
        self.websocketIP = data['websocketIP']
        self.websocketPort = data['websocketPort']
        self.websocketSecret = data['websocketSecret']
        self.slobsIP = data['slobsIP']
        self.slobsPort = data['slobsPort']
        self.sceneInGame = data['sceneInGame']
        self.sceneOutOfGame = data['sceneOutOfGame']
        self.sceneReplay = data['sceneReplay']
        self.sceneObserving = data['sceneObserving']
        self.sceneLobby = data['sceneLobby']
        self.sceneScoreScreen = data['sceneScoreScreen']
        self.sceneProfile = data['sceneProfile']
        self.sceneHome = data['sceneHome']
        self.sceneCampaign = data['sceneCampaign']
        self.sceneMultiplayer = data['sceneMultiplayer']
        self.sceneReplaysMenu = data['sceneReplaysMenu']
        self.sceneCollection = data['sceneCollection']
        self.sceneCustom = data['sceneCustom']
        self.switchOnLoading = data['switchOnLoading']