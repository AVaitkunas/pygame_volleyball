import pygame

from settings import PLAYER_SIZE, SCREEN_WIDTH


class PlayerView:
    def __init__(self, surface, font):
        """Object that is responsible only for player image representation."""
        self.surface = surface
        self.font = font
        player_image = pygame.image.load("views/player.png")
        self.image = pygame.transform.scale(player_image, (PLAYER_SIZE,) * 2)

    def render_player(self, destination_rect, is_side_left, points):
        """Display player image on surface and show current player points."""
        self.surface.blit(self.image, destination_rect)
        self.render_player_points(points=points, is_side_left=is_side_left)

    def render_player_points(self, points, is_side_left):
        """Blit on surface current player points."""
        points_text = self.font.render(str(points), False, pygame.Color("black"))
        points_rect = (SCREEN_WIDTH / 4 if is_side_left else SCREEN_WIDTH / 4 * 3, 0)
        self.surface.blit(points_text, points_rect)
