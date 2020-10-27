import pygame
from settings import (PLAYER_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, GRAVITY,
                      Controls, WALL_WIDTH, PLAYER_SPEED_X, PLAYER_SPEED_Y)


class Player(pygame.sprite.Sprite):
    def __init__(self, controls: Controls, is_side_left: bool = True):
        super().__init__()

        start_position = 0 if is_side_left else SCREEN_WIDTH - PLAYER_SIZE
        self.rect = pygame.Rect(start_position, SCREEN_HEIGHT - PLAYER_SIZE - WALL_WIDTH, PLAYER_SIZE, PLAYER_SIZE)

        self.speed_x = PLAYER_SPEED_X
        self.speed_y = PLAYER_SPEED_Y
        self.is_moving_left = False
        self.is_moving_right = False
        self.is_in_jump = False
        self.is_side_left = is_side_left
        self.points = 0
        self.consecutive_hits = 0
        self.won_match = False
        self.controls = controls

    def start_move(self, key):
        if key == self.controls.left:
            self.is_moving_right = False
            self.is_moving_left = True
        elif key == self.controls.right:
            self.is_moving_right = True
            self.is_moving_left = False
        elif key == self.controls.jump:
            self.is_in_jump = True

    def end_move(self, key):
        if key == self.controls.left:
            self.is_moving_left = False
        elif key == self.controls.right:
            self.is_moving_right = False

    def move_left_stopped(self):
        self.is_moving_left = False

    def move_right_stopped(self):
        self.is_moving_right = False

    def _jump(self):
        self.speed_y += GRAVITY * 2
        if self.rect.bottom + self.speed_y >= SCREEN_HEIGHT:
            self.rect = self.rect.move(0, SCREEN_HEIGHT - self.rect.bottom)
            self.is_in_jump = False
            self.speed_y = PLAYER_SPEED_Y
        self.rect = self.rect.move(0, self.speed_y)

    def make_move(self):
        end_point = SCREEN_WIDTH / 2 if self.is_side_left else SCREEN_WIDTH
        start_point = 0 if self.is_side_left else SCREEN_WIDTH / 2
        if self.is_moving_left and self.rect.left > start_point:
            self.rect = self.rect.move(-self.speed_x, 0)
        if self.is_moving_right and self.rect.right < end_point:
            self.rect = self.rect.move(self.speed_x, 0)
        if self.is_in_jump:
            self._jump()


