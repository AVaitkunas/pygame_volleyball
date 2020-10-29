import json
import pygame
from _thread import start_new_thread
import socket

from event_manager import KeyboardPressEvent, KeyboardReleaseEvent, TickEvent
from game_engine import decode_event
from models.game_state import GameState

# ===
from settings import FPS

server = "192.168.1.227"
port = 5555

socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    socket_connection.bind((server, port))
except socket.error as e:
    print(str(e))

socket_connection.listen(2)
print("Waiting for connections. Server is running.")
clock = pygame.time.Clock()
# ===

game_state = GameState()
game_info = {}


def update_game_info():
    game_info["player1_x"] = game_state.player1.rect.x
    game_info["player1_y"] = game_state.player1.rect.y
    game_info["player1_points"] = game_state.player1.points
    game_info["player2_x"] = game_state.player2.rect.x
    game_info["player2_y"] = game_state.player2.rect.y
    game_info["player2_points"] = game_state.player2.points
    game_info["ball_x"] = game_state.ball.rect.x
    game_info["ball_y"] = game_state.ball.rect.y


update_game_info()


def threaded_client(connection_, player):
    connection_.send(json.dumps(game_info).encode())

    while True:

        # read keyboard event for play
        # update player state
        # send all game_info to everyone
        try:
            data_received = connection_.recv(2048)
        except Exception as e:
            print(str(e))
            break
        if not data_received:
            print("Disconnected")
            break

        event, value = decode_event(data_received.decode())
        if TickEvent.__name__ in event:
            game_state.handle_game_tick_event()
            game_state.check_game_rules_violation()
            game_state.calculate_points_and_start_new_match()

        elif KeyboardPressEvent.__name__ in event:
            game_state.handle_start_move_event(key=value)
        elif KeyboardReleaseEvent.__name__ in event:
            game_state.handle_end_move_event(key=value)

        # always update players and ball positions
        update_game_info()
        connection_.sendall(json.dumps(game_info).encode())
        # clock.tick(FPS)

    print("Lost connection")
    connection_.close()


current_player = 0
while True:
    connection, address = socket_connection.accept()
    print(f"Connected to:{address}")
    start_new_thread(threaded_client, (connection, current_player))
    current_player += 1
