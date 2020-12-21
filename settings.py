from typing import NamedTuple

import pygame


class Controls(NamedTuple):
    left: int
    right: int
    jump: int


# Screen

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
WALL_WIDTH = 10
FPS = 30

# Ball
BALL_GRAVITY = 0.5
AIR_FRICTION = 0.99
BALL_SIZE = 60
ELASTICITY = 0.9

# Net
NET_HEIGHT = 300
NET_WIDTH = 2

# Player
PLAYER_SPEED_X = 8
PLAYER_SPEED_Y = -20
PLAYER_SIZE = 100
PLAYER_STRENGTH = 17
PLAYER_GRAVITY = 0.9

PLAYER_1_CONTROLS = Controls(left=pygame.K_LEFT, right=pygame.K_RIGHT, jump=pygame.K_UP)
PLAYER_2_CONTROLS = Controls(left=ord('a'), right=ord('d'), jump=ord('w'))

# Network messages framing
FRAME_START = b"\x02"
FRAME_END = b"\x03"

# Network socket connection
IP = "192.168.1.227"
PORT = 5555


# todo issues:
#  * Change colors of the players
#  * Ball sometimes stucks into the net if lands directly from above
#  * add a popup when one player wins (reaches 21 or sth).
#  * add 3s pause after game point
#  * when pause is active while multiplayer -> only one window will see "PAUSED" on the screen.
#  * REFACTOR THE GAME
#  * implement computer player

