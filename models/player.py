import pygame
from settings import (PLAYER_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, Controls,
                      WALL_WIDTH, PLAYER_SPEED_X, PLAYER_SPEED_Y, PLAYER_GRAVITY)


class Movement:
    def __init__(self):
        self.left = False
        self.right = False
        self.in_jump = False

    def move_left(self):
        self.left = True
        self.right = False

    def move_right(self):
        self.left = False
        self.right = True

    def jump(self):
        self.in_jump = True

    def stop_vertical(self):
        self.left = False
        self.right = False


class Player:
    def __init__(self, controls: Controls, is_side_left: bool = True):
        super().__init__()
        self.controls = controls
        self.movement = Movement()

        start_position = 0 if is_side_left else SCREEN_WIDTH - PLAYER_SIZE
        self.rect = pygame.Rect(start_position, SCREEN_HEIGHT - PLAYER_SIZE - WALL_WIDTH, PLAYER_SIZE, PLAYER_SIZE)

        self.is_side_left = is_side_left
        self.boundary_x = 0 if is_side_left else SCREEN_WIDTH / 2

        self.speed_x = PLAYER_SPEED_X
        self.speed_y = PLAYER_SPEED_Y

        self.points = 0
        self.consecutive_hits = 0
        self.won_match = False

    def start_move(self, key):
        if key == self.controls.left:
            self.movement.move_left()
        elif key == self.controls.right:
            self.movement.move_right()
        elif key == self.controls.jump:
            self.movement.jump()

    def end_move(self, key):
        if key in (self.controls.left, self.controls.right):
            self.movement.stop_vertical()

    def _jump(self):
        self.speed_y += PLAYER_GRAVITY
        if self.rect.bottom + self.speed_y >= SCREEN_HEIGHT:
            self.rect = self.rect.move(0, SCREEN_HEIGHT - self.rect.bottom)
            self.movement.in_jump = False
            self.speed_y = PLAYER_SPEED_Y
        self.rect = self.rect.move(0, self.speed_y)

    def make_move(self):
        if self.movement.left and self.rect.left > self.boundary_x:
            self.rect = self.rect.move(-self.speed_x, 0)
        if self.movement.right and self.rect.right < self.boundary_x + SCREEN_WIDTH / 2:
            self.rect = self.rect.move(self.speed_x, 0)
        if self.movement.in_jump:
            self._jump()
