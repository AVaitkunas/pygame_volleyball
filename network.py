import json
import select
import socket

from event_manager import Listener, StateChangeEvent
from models.state_machine import States
from settings import FRAME_START, FRAME_END
from views.menu import GameModes


class Network(Listener):
    def __init__(self, event_manager, game_engine):
        super().__init__(event_manager)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setblocking(False)
        self.server = "192.168.1.227"
        self.port = 5555
        self.address = (self.server, self.port)
        self.game_info = None
        self.game_engine = game_engine
        self.connected = False
        self.bytes_buffer = b''

    def notify(self, event):
        if isinstance(event, StateChangeEvent) and event.state == States.STATE_PLAY and self.game_engine.game_mode == GameModes.MULTI_PLAYER_ONLINE:
            try:
                self.client.connect(self.address)
            except Exception as e:
                print(str(e))
            self.connected = True

        if self.connected:
            socket_not_empty, *_ = select.select([self.client], [], [], 0)

            if socket_not_empty:
                self.bytes_buffer = b''.join([self.bytes_buffer, self.client.recv(2048)])

                end_idx = self.bytes_buffer.rfind(FRAME_END)
                if end_idx == -1:
                    return
                start_idx = self.bytes_buffer[:end_idx].rfind(FRAME_START)
                if start_idx == -1:
                    return
                self.game_info = json.loads(self.bytes_buffer[start_idx+1:end_idx].decode())
                self.bytes_buffer = b''

    def send(self, data):
        if not isinstance(data, bytes):
            raise ValueError("Data to send is not of type bytes")
        data_to_send = b''.join([FRAME_START, data, FRAME_END])
        try:
            self.client.send(data_to_send)
        except Exception as e:
            print(str(e))
