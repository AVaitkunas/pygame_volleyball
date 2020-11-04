import json
import socket

from event_manager import Listener, StateChangeEvent, TickEvent
from models.state_machine import States
from views.menu import GameModes


class Network(Listener):
    def __init__(self, event_manager, game_engine):
        super().__init__(event_manager)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.server = "192.168.1.227"
        self.server = "172.28.10.131"
        self.port = 5555
        self.address = (self.server, self.port)
        self.game_info = None
        self.game_engine = game_engine
        self.connected = False

    def notify(self, event):
        if isinstance(event, StateChangeEvent) and event.state == States.STATE_PLAY and self.game_engine.game_mode == GameModes.MULTI_PLAYER_ONLINE:
            try:
                self.client.connect(self.address)
            except Exception as e:
                print(str(e))
            self.connected = True

        if isinstance(event, TickEvent) and self.connected:
            data = self.client.recv(2048)
            self.game_info = json.loads(data.decode())


    #
    # def connect(self):
    #     try:
    #         self.client.connect(self.address)
    #         data = self.client.recv(2048)
    #         return json.loads(data.decode())
    #     except Exception as e:
    #         print(str(e))

    def send(self, data):
        try:
            self.client.send(data)
        except Exception as e:
            print(str(e))
