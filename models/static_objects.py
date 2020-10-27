import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, NET_WIDTH, NET_HEIGHT


class Net(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.sprite.Rect(SCREEN_WIDTH / 2 - NET_WIDTH, SCREEN_HEIGHT, 2 * NET_WIDTH, - NET_HEIGHT)
        # todo bug appeared when moved drawing to views... ???


class Wall(pygame.sprite.Sprite):
    def __init__(self, *groups, rect=(0,) * 4):
        super().__init__(*groups)
        self.rect = pygame.Rect(rect)
