import sys
from math import sqrt

import pygame

# SETTINGS
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
WALL_WIDTH = 10

FPS = 30
GRAVITY = 0.5
AIR_FRICTION = 0.99
NET_HEIGHT = 300
NET_WIDTH = 5
PLAYER_SIZE = 100
PLAYER_STRENGTH = 20

BALL_SIZE = 50

WHITE = (225,) * 3
BLACK = (0,) * 3

pygame.font.init()
FONT = pygame.font.SysFont('Comic Sans MS', 30)

display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
display.fill(WHITE)
pygame.display.set_caption("Volleyball")


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
        self.elasticity = 0.8
        self.has_bounced_x = False
        self.has_bounced_y = False

    def move(self):
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

    def hit(self, object_rect, strength=15):
        delta_x = self.rect.centerx - object_rect.centerx
        delta_y = self.rect.centery - object_rect.centery
        normalization_factor = strength / sqrt(delta_x ** 2 + delta_y ** 2)
        self.speed_x = normalization_factor * delta_x
        self.speed_y = normalization_factor * delta_y

    def bounce_x(self):
        self.speed_x *= -1
        self.has_bounced_x = True

    def bounce_y(self):
        self.speed_y *= -1
        self.has_bounced_y = True

    def show(self, surface):
        surface.blit(self.image, self.rect)


class Player(pygame.sprite.Sprite):
    def __init__(self, start_position=0, is_side_left=True, *groups):
        super().__init__(*groups)
        player_image = pygame.image.load("player.png")
        self.image = pygame.transform.scale(player_image, (PLAYER_SIZE,) * 2)
        self.rect = self.image.get_rect()
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

    def show(self, surface):
        surface.blit(self.image, self.rect)
        self.show_points(surface=surface)

    def show_points(self, surface):
        points_text = FONT.render(str(self.points), False, BLACK)
        position = SCREEN_WIDTH / 4 if self.is_side_left else SCREEN_WIDTH / 4 * 3
        surface.blit(points_text, (position, 0))


class Net(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.rect = pygame.draw.rect(
            display, BLACK, (SCREEN_WIDTH / 2 - NET_WIDTH, SCREEN_HEIGHT, 2 * NET_WIDTH, - NET_HEIGHT)
        )

    def show(self, surface):
        pygame.draw.rect(surface, BLACK, self.rect)


class Wall(pygame.sprite.Sprite):
    def __init__(self, *groups, rect=(0,) * 4):
        super().__init__(*groups)
        self.rect = pygame.draw.rect(display, WHITE, rect)

    def show(self, surface):
        pygame.draw.rect(surface, BLACK, self.rect)


pygame.init()

clock = pygame.time.Clock()
volleyball_ball = Ball()
player1 = Player(start_position=SCREEN_WIDTH - PLAYER_SIZE, is_side_left=False)
player2 = Player(start_position=0, is_side_left=True)
net = Net()

vertical_walls = pygame.sprite.Group()
horizontal_walls = pygame.sprite.Group()
left_wall = Wall(vertical_walls, rect=(0, 0, WALL_WIDTH, SCREEN_HEIGHT))
right_wall = Wall(vertical_walls, rect=(SCREEN_WIDTH - WALL_WIDTH, 0, WALL_WIDTH, SCREEN_HEIGHT))
bottom_wall = Wall(horizontal_walls, rect=(0, SCREEN_HEIGHT - WALL_WIDTH, SCREEN_WIDTH, WALL_WIDTH))
upper_wall = Wall(horizontal_walls, rect=(0, 0, SCREEN_WIDTH, WALL_WIDTH))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player1.move_left_started()
            if event.key == pygame.K_RIGHT:
                player1.move_right_started()
            if event.key == pygame.K_UP:
                player1.move_jump()

            if event.key == ord('a'):
                player2.move_left_started()
            if event.key == ord('d'):
                player2.move_right_started()
            if event.key == ord('w'):
                player2.move_jump()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player1.move_left_stopped()
            if event.key == pygame.K_RIGHT:
                player1.move_right_stopped()

            if event.key == ord('a'):
                player2.move_left_stopped()
            if event.key == ord('d'):
                player2.move_right_stopped()

    display.fill(WHITE)
    net.show(surface=display)
    player1.show(surface=display)
    player2.show(surface=display)
    volleyball_ball.show(surface=display)

    volleyball_ball.move()
    player1.make_move()
    player2.make_move()
    # BALL dynamics
    if pygame.sprite.collide_rect(player1, volleyball_ball):
        volleyball_ball.hit(player1.rect, strength=PLAYER_STRENGTH)
        player1.consecutive_hits += 1
        player2.consecutive_hits = 0

    if pygame.sprite.collide_rect(player2, volleyball_ball):
        volleyball_ball.hit(player2.rect, strength=PLAYER_STRENGTH)
        player2.consecutive_hits += 1
        player1.consecutive_hits = 0

    if pygame.sprite.collide_rect(net, volleyball_ball):
        volleyball_ball.bounce_x()

    if pygame.sprite.spritecollide(volleyball_ball, vertical_walls, False):
        volleyball_ball.bounce_x()

    if pygame.sprite.spritecollide(volleyball_ball, horizontal_walls, False):
        volleyball_ball.bounce_y()

    # check violation of the rules
    if pygame.sprite.collide_rect(volleyball_ball, bottom_wall):
        if volleyball_ball.rect.centerx < SCREEN_WIDTH / 2:
            player2.lost_match = True
        else:
            player1.lost_match = True
    if player1.consecutive_hits > 3:
        player1.lost_match = True
    if player2.consecutive_hits > 3:
        player2.lost_match = True

    if player2.lost_match:
        player1.points += 1
    if player1.lost_match:
        player2.points += 1

    if any([player1.lost_match, player2.lost_match]):
        position = SCREEN_WIDTH / 4 if player1.lost_match else SCREEN_WIDTH / 4 * 3
        volleyball_ball = Ball(position=round(position))
        player1.lost_match = False
        player2.lost_match = False
        player1.consecutive_hits = 0
        player2.consecutive_hits = 0

    pygame.display.flip()
    clock.tick(FPS)
