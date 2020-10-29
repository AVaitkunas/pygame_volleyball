import json
import socket


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.1.227"
        self.port = 5555
        self.address = (self.server, self.port)
        self.game_info = self.connect()

    def connect(self):
        try:
            self.client.connect(self.address)
            data = self.client.recv(2048)
            return json.loads(data.decode())
        except Exception as e:
            print(str(e))

    def send(self, data):
        try:
            self.client.send(data)
            received_data = self.client.recv(2048)
            self.game_info = json.loads(received_data.decode())
        except Exception as e:
            print(str(e))
