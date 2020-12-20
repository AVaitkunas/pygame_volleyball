import json
import select

import pygame
import socket
from collections import deque
from dataclasses import dataclass
from threading import Thread, Lock

import uuid

from event_manager import KeyboardPressEvent, KeyboardReleaseEvent
from game_engine import decode_event
from models.game_state import GameState
from settings import FPS, FRAME_START, FRAME_END, IP, PORT


@dataclass
class ClientInfo:
    connection: socket
    address: str
    unique_id: uuid.UUID
    opponent_id: uuid.UUID = None
    game_id: uuid.UUID = None


class GameThread(Thread):
    def __init__(self, game_state: GameState, client_1_info: ClientInfo, client_2_info: ClientInfo):
        super().__init__()
        self.player_1_info = client_1_info
        self.player_2_info = client_2_info
        self.game_state = game_state
        self.game_info = {}
        self.clock = pygame.time.Clock()
        self.lock = Lock()
        self.update_game_info()

    def run(self):
        while True:
            self.handle_tick_event()
            self.update_game_info()
            self.clock.tick(FPS)

    def update_game_info(self):
        with self.lock:
            self.game_info["player1_x"] = self.game_state.player1.rect.x
            self.game_info["player1_y"] = self.game_state.player1.rect.y
            self.game_info["player1_points"] = self.game_state.player1.points
            self.game_info["player2_x"] = self.game_state.player2.rect.x
            self.game_info["player2_y"] = self.game_state.player2.rect.y
            self.game_info["player2_points"] = self.game_state.player2.points
            self.game_info["ball_x"] = self.game_state.ball.rect.x
            self.game_info["ball_y"] = self.game_state.ball.rect.y

    def get_game_state_info_message(self):
        encoded_game_info = b"".join([FRAME_START, json.dumps(self.game_info).encode(), FRAME_END])
        with self.lock:
            return encoded_game_info

    def handle_tick_event(self):
        with self.lock:
            self.game_state.handle_game_tick_event()
            self.game_state.check_game_rules_violation()
            self.game_state.calculate_points_and_start_new_match()

    def handle_start_move(self, player_id, key_value):
        with self.lock:
            if player_id == self.player_1_info.unique_id:
                self.game_state.handle_start_move_event_player_1(key=key_value)
            elif player_id == self.player_2_info.unique_id:
                self.game_state.handle_start_move_event_player_2(key=key_value)
            else:
                raise ValueError("Incorrect player ID provided")

    def handle_end_move(self, player_id, key_value):
        with self.lock:
            if player_id == self.player_1_info.unique_id:
                self.game_state.handle_end_move_event_player_1(key=key_value)
            elif player_id == self.player_2_info.unique_id:
                self.game_state.handle_end_move_event_player_2(key=key_value)
            else:
                raise ValueError("Incorrect player ID provided")


class ClientThread(Thread):
    def __init__(self, game_state_thread: GameThread, client_info: ClientInfo):
        super().__init__()
        self.client_info = client_info
        self.socket = client_info.connection
        self.socket.setblocking(0)
        self.game_state_thread = game_state_thread
        self.lock = Lock()
        self.clock = pygame.time.Clock()

    def run(self):
        game_state_info = self.game_state_thread.get_game_state_info_message()
        self.socket.send(game_state_info)
        while True:
            self.clock.tick(FPS)
            game_state_info = self.game_state_thread.get_game_state_info_message()
            self.socket.send(game_state_info)

            ready, *_ = select.select([self.socket], [], [], 0)
            if ready:
                try:
                    data_received = self.socket.recv(2048)
                except Exception as e:
                    print(str(e))
                    break

                if not data_received:
                    continue

                end_idx = data_received.rfind(FRAME_END)
                if end_idx == -1:
                    continue
                start_idx = data_received[:end_idx].rfind(FRAME_START)
                if start_idx == -1:
                    continue

                event, value = decode_event(data_received[start_idx+1:end_idx].decode())

                with self.lock:
                    if KeyboardPressEvent.__name__ in event:
                        self.game_state_thread.handle_start_move(player_id=self.client_info.unique_id, key_value=value)
                    elif KeyboardReleaseEvent.__name__ in event:
                        self.game_state_thread.handle_end_move(player_id=self.client_info.unique_id, key_value=value)

        print("Lost connection")
        self.socket.close()


class Server:
    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port
        self.socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.game_state = GameState()
        self.games = {}
        self.clients = {}
        self.clients_waiting_for_opponents = deque()

        try:
            self.socket_connection.bind((ip, port))
        except socket.error as e:
            print(str(e))

        self.socket_connection.listen(20)
        print("Waiting for connections. Server is running.")

    def run(self):
        while True:
            connection, address = self.socket_connection.accept()
            print(f"Connected to: {address}")
            self.register_client(connection, address)
            game_id = self.start_new_game()
            if game_id:
                print(f"Game started. Game ID: {game_id}")

    def register_client(self, connection, address):
        client_id = uuid.uuid1()
        client_info = ClientInfo(connection=connection, address=address, unique_id=client_id)
        self.clients[client_id] = client_info
        self.clients_waiting_for_opponents.append(client_info)

    def start_new_game(self):
        if len(self.clients_waiting_for_opponents) < 2:
            return

        player_1 = self.clients_waiting_for_opponents.popleft()
        player_2 = self.clients_waiting_for_opponents.popleft()

        player_1.opponent_id = player_2.unique_id
        player_2.opponent_id = player_1.unique_id

        # todo think if there is need to pot to INIT method of thread class
        game_state = GameState()
        game_id = uuid.uuid1()
        self.games[game_id] = game_state

        self.clients[player_1.unique_id].game_id = game_id
        self.clients[player_2.unique_id].game_id = game_id

        game_thread = GameThread(
            game_state=game_state,
            client_1_info=self.clients[player_1.unique_id],
            client_2_info=self.clients[player_2.unique_id],
        )

        player_1_thread = ClientThread(
            game_state_thread=game_thread,
            client_info=self.clients[player_1.unique_id]
        )
        player_2_thread = ClientThread(
            game_state_thread=game_thread,
            client_info=self.clients[player_2.unique_id]
        )

        game_thread.start()
        player_1_thread.start()
        player_2_thread.start()

        return game_id


if __name__ == '__main__':
    # server = Server(ip="172.28.10.131", port=5555)
    server = Server(ip=IP, port=PORT)
    server.run()
