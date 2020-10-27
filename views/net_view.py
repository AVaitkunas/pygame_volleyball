import pygame


class NetView:
    def __init__(self, surface):
        self.surface = surface

    def render(self, destination_rect):
        pygame.draw.rect(self.surface, pygame.Color("black"), destination_rect)
