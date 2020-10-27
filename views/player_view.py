import pygame

from settings import PLAYER_SIZE


class PlayerView:
    def __init__(self, surface):
        self.surface = surface

        player_image = pygame.image.load("views/player.png")
        self.image = pygame.transform.scale(player_image, (PLAYER_SIZE,) * 2)
        self.rect = self.image.get_rect()

    def render_player(self, destination_rect):
        self.surface.blit(self.image, destination_rect)

    def render_player_points(self, points, font, destination_rect):
        points_text = font.render(str(points), False, pygame.Color("black"))
        self.surface.blit(points_text, destination_rect)
