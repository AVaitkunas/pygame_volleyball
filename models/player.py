import pygame
from settings import PLAYER_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, GRAVITY, Controls


class Player(pygame.sprite.Sprite):
    def __init__(self, controls: Controls, is_side_left: bool = True):
        super().__init__()

        # todo image should go to image player view object
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
        self.controls = controls

    def start_move(self, key):
        if key == self.controls.left:
            self.is_moving_right = False
            self.is_moving_left = True
        elif key == self.controls.right:
            self.is_moving_right = True
            self.is_moving_left = False
        elif key == self.controls.jump:
            self.is_in_jump = True

    def end_move(self, key):
        if key == self.controls.left:
            self.is_moving_left = False
        elif key == self.controls.right:
            self.is_moving_right = False


    def move_left_stopped(self):
        self.is_moving_left = False

    def move_right_stopped(self):
        self.is_moving_right = False

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

    # todo shoe must go in views
    def show(self, surface, font):
        surface.blit(self.image, self.rect)
        self.show_points(surface=surface, font=font)

    def show_points(self, surface, font):
        points_text = font.render(str(self.points), False, pygame.Color("black"))
        position = SCREEN_WIDTH / 4 if self.is_side_left else SCREEN_WIDTH / 4 * 3
        surface.blit(points_text, (position, 0))
