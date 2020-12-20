import pygame


class NetView:
    def __init__(self, surface):
        """Creates object responsible for representation of volleyball net."""
        self.surface = surface

    def render(self, destination_rect):
        """Draws NET on the game surface."""
        pygame.draw.rect(self.surface, pygame.Color("black"), destination_rect)
