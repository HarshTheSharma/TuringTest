import socket
import threading
import random
import urllib.request
class Server:
    def __init__(self):
        self.externalIP = urllib.request.urlopen('https://v4.ident.me').read().decode('utf8')
        self.port = random.randint(48000, 49151)
        print("CONNECT TO " + self.externalIP + ":" + self.port)