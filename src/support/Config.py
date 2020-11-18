import json, os

def Config():
    if _Config._instance is None:
        _Config._instance = _Config()
    return _Config._instance

class _Config:
    _instance = None

    def __init__(self):
        self.filename = "data/nydus.json"
        self.fromData({
                "ip": "localhost",
                "port": "6119",
                "size": None,
                "pos": None,
                "log_size": None,
                "log_pos": None,
                "log_to_file": False,
                "running": True,
                "plugins": {},
                "usernames": [],
                "recentUsernames": []
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
                "ip": self.ip,
                "port": self.port,
                "size": self.size,
                "pos": self.pos,
                "log_size": self.log_size,
                "log_pos": self.log_pos,
                "log_to_file": self.log_to_file,
                "running": self.running,
                "plugins": self.plugins,
                "usernames": self.usernames,
                "recentUsernames": self.recentUsernames
            }, outfile, indent=4, sort_keys=True)

    def fromData(self, data):
        self.ip = data['ip']
        self.port = data['port']
        self.size = data['size']
        self.pos = data['pos']
        self.log_size = data['log_size']
        self.log_pos = data['log_pos']
        self.log_to_file = data['log_to_file']
        self.running = data['running']
        self.plugins = data['plugins']
        self.usernames = data['usernames']
        self.recentUsernames = data['recentUsernames']
