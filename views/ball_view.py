import pygame

from settings import BALL_SIZE


class BallView:
    def __init__(self, surface):
        self.surface = surface

        ball_image = pygame.image.load("views/ball.png")
        self.image = pygame.transform.scale(ball_image, (BALL_SIZE,) * 2)

    def render(self, destination_rect):
        self.surface.blit(self.image, destination_rect)
