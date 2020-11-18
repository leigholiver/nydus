import json, os
from datetime import datetime
from support.Config import Config

def Logger(base_path = os.path.abspath(".")):
    if _Logger._instance is None:
        _Logger._instance = _Logger(base_path)
    return _Logger._instance

class _Logger:
    _instance = None
    messages = []
    watchers = []

    def __init__(self, base_path):
        self.filename = base_path + "/data/logs/nydus-" + datetime.now().strftime("%Y-%m-%d-%H-%M") + ".txt"
        self.log("Logging to " + self.filename)

    def log(self, message):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = "[" + now + "] " + message.rstrip(os.linesep)

        if Config().log_to_file:
            f = open(self.filename, "w+")
            f.write(message + "\n")
            f.close()

        # save for console
        self.messages.append(message)
        for watcher in self.watchers:
            func = getattr(watcher['obj'], watcher['callback'])
            func(message)

    def attach(self, obj, callback):
        self.watchers.append({ 'obj': obj, 'callback': callback })

    def dump(self):
        try:
            f = open(self.filename, "w")
            for message in self.messages:
                f.write(message + "\n")
            f.close()
        except Exception as e:
            self.log("[Logger] Log dump failed: " + str(e))

    def write(self, message):
        self.log(message)

    def flush(self):
        pass
