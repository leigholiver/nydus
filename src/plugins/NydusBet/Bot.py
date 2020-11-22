import sys, socket, re, time
from PyQt5.QtCore import QThread, pyqtSignal

class Bot(QThread):
    command = pyqtSignal(str, str, list)
    host = "irc.twitch.tv"
    port = 6667

    def __init__(self, parent, data):
        QThread.__init__(self)
        self.parent = parent
        self.data = data
        self.data['channel'] = "#" + self.data['channel'].lower()
        self.con = socket.socket()
        self.parent.sendMessage.connect(self.sendMessage)
        self.stopping = False
    
    def sendMessage(self, message):
        self.parent.log("Sending " + message + " to " + self.data['channel'])
        self.send_message(self.data['channel'], message)

    def handleMessage(self, sender, message):
        delim = "!"
        if message.startswith(delim):
            params = message.split(" ")
            params.remove('')
            cmd = params.pop(0).replace(delim, "")
            self.command.emit(sender, cmd, params)

    def run(self):
        try:
            self.con.connect((self.host, self.port))
        except:
            print("couldnt connect, exiting")
            return 
            
        self.con.send(bytes('PASS %s\r\n' % self.data['oauth'], 'UTF-8'))
        self.con.send(bytes('NICK %s\r\n' % self.data['username'], 'UTF-8'))
        self.con.send(bytes('JOIN %s\r\n' % self.data['channel'], 'UTF-8'))

        data = ""
        while not self.stopping:
            try:
                data = data+self.con.recv(1024).decode('UTF-8')
                data_split = re.split(r"[~\r\n]+", data)
                data = data_split.pop()

                for line in data_split:
                    line = str.rstrip(line)
                    line = str.split(line)

                    if len(line) >= 1:
                        if line[0] == 'PING':
                            self.send_pong(line[1])

                        if line[1] == 'PRIVMSG':
                            sender = self.get_sender(line[0])
                            message = self.get_message(line)
                            self.handleMessage(sender, message)

            except socket.error as e:
                self.parent.log("Twitch chat socket error: [%s] %s" % (e.__class__.__name__, str(e)))
                time.sleep(2)

            except socket.timeout:
                self.parent.log("Twitch chat socket timeout")

    def stop(self):
        self.stopping = True
        self.exit()
        self.wait()

    def send_pong(self, msg):
        self.con.send(bytes('PONG %s\r\n' % msg, 'UTF-8'))

    def send_message(self, chan, msg):
        self.con.send(bytes('PRIVMSG %s :%s\r\n' % (chan, msg), 'UTF-8'))

    def get_sender(self, msg):
        result = ""
        for char in msg:
            if char == "!":
                break
            if char != ":":
                result += char
        return result

    def get_message(self, msg):
        result = ""
        i = 3
        length = len(msg)
        while i < length:
            result += msg[i] + " "
            i += 1
        result = result.lstrip(':')
        return result