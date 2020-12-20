from math import sqrt

import pygame

from settings import BALL_SIZE, BALL_GRAVITY, AIR_FRICTION, WALL_WIDTH, PLAYER_SPEED_Y, ELASTICITY


class Ball(pygame.sprite.Sprite):
    def __init__(self, position=10, *groups):
        super().__init__(*groups)
        self.speed_x = 0
        self.speed_y = 0
        self.rect = pygame.Rect(position, WALL_WIDTH, BALL_SIZE, BALL_SIZE)

    def make_move(self):
        """Makes ball move. Gravity and air friction are taken into account."""
        self.speed_y += BALL_GRAVITY
        self.speed_y *= AIR_FRICTION

        self.speed_x *= AIR_FRICTION

        self.rect = self.rect.move(self.speed_x, self.speed_y)

    def hit(self, object_rect, strength, speed_in_y=0, is_in_jump=False):
        """Perform ball hit."""
        # Get information to which direction ball will be hit.
        # Depends on positions where the ball and hitting have object touched
        delta_x = self.rect.centerx - object_rect.centerx
        delta_y = self.rect.centery - object_rect.centery
        normalization_factor = strength / sqrt(delta_x ** 2 + delta_y ** 2)

        # In case the hit was performed while hitting object was in the jump,
        # speed to the ball is added/minimized (hitting object rises/falls).
        if is_in_jump:
            if speed_in_y < 0:
                normalization_factor *= 1 + (speed_in_y / PLAYER_SPEED_Y) * 0.5
            else:
                normalization_factor *= 1 - (speed_in_y / PLAYER_SPEED_Y) * 0.5

            # handles the overlap between hitting object and ball rects
            clip = object_rect.clip(self.rect)
            if abs(clip.h) + abs(speed_in_y) > abs(self.speed_y):
                self.rect.y -= abs(clip.h) + abs(speed_in_y) - abs(self.speed_y)

        self.speed_x = normalization_factor * delta_x
        self.speed_y = normalization_factor * delta_y

    def bounce_x(self, object_rect):
        """Bounce from vertical objects i.e. change velocity in direction of X.
        Speed on bounce is dependent on elasticity of the ball.
        """
        # handles stuck to the vertical objects
        clip = object_rect.clip(self.rect)
        self.rect.x = self.rect.x - clip.w if self.speed_x > 0 else self.rect.x + clip.w

        self.speed_x *= -ELASTICITY

    def bounce_y(self, object_rect):
        """Bounce from horizontal objects i.e. change velocity in direction of Y.
        Speed on bounce is dependent on elasticity of the ball.
        """
        # handles stuck to the horizontal objects
        clip = object_rect.clip(self.rect)
        self.rect.y = self.rect.y - clip.h if self.speed_y > 0 else self.rect.y + clip.h

        self.speed_y *= -ELASTICITY
