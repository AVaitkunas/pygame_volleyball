import pygame


class Wall(pygame.sprite.Sprite):
    def __init__(self, *groups, rect=(0,) * 4):
        super().__init__(*groups)
        self.rect = pygame.Rect(rect)
