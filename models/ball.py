from math import sqrt

import pygame

from settings import BALL_SIZE, BALL_GRAVITY, AIR_FRICTION, WALL_WIDTH, PLAYER_SPEED_Y


class Ball(pygame.sprite.Sprite):
    def __init__(self, position=10, *groups):
        super().__init__(*groups)
        self.speed_x = 0
        self.speed_y = 0

        self.rect = pygame.Rect(position, WALL_WIDTH, BALL_SIZE, BALL_SIZE)
        self.elasticity = 0.9
        self.has_bounced_x = False
        self.has_bounced_y = False

    def make_move(self):
        """Makes ball move. Gravity is taken into account."""
        self.speed_y += BALL_GRAVITY
        self.speed_x *= AIR_FRICTION

        self.rect = self.rect.move(self.speed_x, self.speed_y)
        if self.has_bounced_x:
            self.speed_x *= self.elasticity
            self.has_bounced_x = False
        if self.has_bounced_y:
            self.speed_y *= self.elasticity
            self.has_bounced_y = False

    def hit(self, object_rect, strength, speed_in_y=0, is_in_jump=0):
        delta_x = self.rect.centerx - object_rect.centerx
        delta_y = self.rect.centery - object_rect.centery
        normalization_factor = strength / sqrt(delta_x ** 2 + delta_y ** 2)
        if is_in_jump:

            if speed_in_y < 0:
                normalization_factor *= 1 + (speed_in_y / PLAYER_SPEED_Y) * 0.5
            else:
                normalization_factor *= 1 - (speed_in_y / PLAYER_SPEED_Y) * 0.5

            clip = object_rect.clip(self.rect)
            if abs(clip.h) + abs(speed_in_y) > abs(self.speed_y):
                self.rect.y -= abs(clip.h) + abs(speed_in_y) - abs(self.speed_y)

        self.speed_x = normalization_factor * delta_x
        self.speed_y = normalization_factor * delta_y

    def bounce_x(self):
        self.speed_x *= -1
        self.has_bounced_x = True

    def bounce_y(self):
        self.speed_y *= -1
        self.has_bounced_y = True
