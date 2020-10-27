from math import sqrt

import pygame

from settings import BALL_SIZE, GRAVITY, AIR_FRICTION, WALL_WIDTH


class Ball(pygame.sprite.Sprite):
    def __init__(self, position=10, *groups):
        super().__init__(*groups)
        self.speed_x = 0
        self.speed_y = 0
        self.is_stopped = False

        self.rect = pygame.Rect(position, WALL_WIDTH, BALL_SIZE, BALL_SIZE)
        self.elasticity = 0.9
        self.has_bounced_x = False
        self.has_bounced_y = False

    def make_move(self):
        """Makes ball move. Gravity is taken into account."""
        if not self.is_stopped:
            self.speed_y += GRAVITY
            self.speed_x *= AIR_FRICTION

            self.rect = self.rect.move(self.speed_x, self.speed_y)
            if self.has_bounced_x:
                self.speed_x *= self.elasticity
                self.has_bounced_x = False
            if self.has_bounced_y:
                self.speed_y *= self.elasticity
                self.has_bounced_y = False

    def hit(self, object_rect, strength=15, offset_x=0, offset_y=0):
        delta_x = self.rect.centerx - object_rect.centerx
        delta_y = self.rect.centery - object_rect.centery
        normalization_factor = strength / sqrt(delta_x ** 2 + delta_y ** 2)
        self.speed_x = normalization_factor * delta_x + offset_x
        self.speed_y = normalization_factor * delta_y + offset_y

    def bounce_x(self):
        self.speed_x *= -1
        self.has_bounced_x = True

    def bounce_y(self):
        self.speed_y *= -1
        self.has_bounced_y = True
