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

# Net
NET_HEIGHT = 300
NET_WIDTH = 5

# Player
PLAYER_SPEED_X = 8
PLAYER_SPEED_Y = -20
PLAYER_SIZE = 100
PLAYER_STRENGTH = 17
PLAYER_GRAVITY = 0.9

PLAYER_1_CONTROLS = Controls(left=pygame.K_LEFT, right=pygame.K_RIGHT, jump=pygame.K_UP)
PLAYER_2_CONTROLS = Controls(left=ord('a'), right=ord('d'), jump=ord('w'))


FRAME_START = b"\x02"
FRAME_END = b"\x03"


# todo issues:
#  1. Ball/player needs to be bouncy
#  2. Change colors of the players
#  3. Ball sometimes stucks into the net if lands directly from above
#  4. add a popup when one player wins (reaches 21 or sth).
#  5. add 3s pause after game point
#  6. implement pause
