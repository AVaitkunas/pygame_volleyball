from math import sqrt

import pygame
from settings import BALL_SIZE, GRAVITY, AIR_FRICTION, SCREEN_WIDTH, PLAYER_SIZE, SCREEN_HEIGHT, NET_WIDTH, NET_HEIGHT


class Ball(pygame.sprite.Sprite):
    def __init__(self, position=10, *groups):
        super().__init__(*groups)
        self.speed_x = 0
        self.speed_y = 0
        self.is_stopped = False
        ball_image = pygame.image.load("ball.png")
        self.image = pygame.transform.scale(ball_image, (BALL_SIZE,) * 2)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(position, 10)
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

    def show(self, surface):
        surface.blit(self.image, self.rect)


class Player(pygame.sprite.Sprite):
    def __init__(self, is_side_left=True, *groups):
        super().__init__(*groups)
        player_image = pygame.image.load("player.png")
        self.image = pygame.transform.scale(player_image, (PLAYER_SIZE,) * 2)
        self.rect = self.image.get_rect()
        start_position = 0 if is_side_left else SCREEN_WIDTH - PLAYER_SIZE
        self.rect = self.rect.move(start_position, SCREEN_HEIGHT - PLAYER_SIZE)
        self.speed_x = 10
        self.speed_y = -10
        self.is_moving_left = False
        self.is_moving_right = False
        self.is_in_jump = False
        self.is_side_left = is_side_left
        self.points = 0
        self.consecutive_hits = 0
        self.lost_match = False

    def move_left_started(self):
        self.is_moving_right = False
        self.is_moving_left = True

    def move_right_started(self):
        self.is_moving_right = True
        self.is_moving_left = False

    def move_left_stopped(self):
        self.is_moving_left = False

    def move_right_stopped(self):
        self.is_moving_right = False

    def move_jump(self):
        self.is_in_jump = True

    def _jump(self):
        self.speed_y += GRAVITY * 2
        if self.rect.bottom + self.speed_y >= SCREEN_HEIGHT:
            self.rect = self.rect.move(0, SCREEN_HEIGHT - self.rect.bottom)
            self.is_in_jump = False
            self.speed_y = -20
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

    def show(self, surface, font):
        surface.blit(self.image, self.rect)
        self.show_points(surface=surface, font=font)

    def show_points(self, surface, font):
        points_text = font.render(str(self.points), False, pygame.Color("black"))
        position = SCREEN_WIDTH / 4 if self.is_side_left else SCREEN_WIDTH / 4 * 3
        surface.blit(points_text, (position, 0))


class Net(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(SCREEN_WIDTH / 2 - NET_WIDTH, SCREEN_HEIGHT, 2 * NET_WIDTH, - NET_HEIGHT)

    def show(self, surface):
        self.rect = pygame.draw.rect(surface, pygame.Color("black"), self.rect)


class Wall(pygame.sprite.Sprite):
    def __init__(self, *groups, rect=(0,) * 4):
        super().__init__(*groups)
        self.rect = pygame.Rect(rect)

    def show(self, surface):
        pygame.draw.rect(surface, pygame.Color("black"), self.rect)
