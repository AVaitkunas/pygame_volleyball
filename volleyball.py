import sys
import pygame

# SETTINGS
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FPS = 30
GRAVITY = 0.5

WHITE = (225,) * 3
BLACK = (0,) * 3

display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
display.fill(WHITE)
pygame.display.set_caption("Volleyball")


class Ball(pygame.sprite.Sprite):
    def __init__(self, diameter=50, *groups):
        super().__init__(*groups)
        self.speed_x = 5
        self.speed_y = 0
        self.is_stopped = False
        ball_image = pygame.image.load("ball.png")
        self.image = pygame.transform.scale(ball_image, (diameter,) * 2)
        self.rect = self.image.get_rect()
        self.elasticity = 0.7

    def move(self):
        """Makes ball move. Gravity is taken into account."""
        if not self.is_stopped:
            self.speed_y += GRAVITY
            # handling of ball appearing bellow screen boundaries
            if self.rect.bottom + self.speed_y < SCREEN_HEIGHT:
                self.rect = self.rect.move(self.speed_x, self.speed_y)
            else:
                self.rect = self.rect.move(self.speed_x, SCREEN_HEIGHT - self.rect.bottom)

            # handling of ball bounces from walls
            if self.rect.right >= SCREEN_WIDTH or self.rect.left < 0:
                self.speed_x *= -self.elasticity
            if self.rect.bottom >= SCREEN_HEIGHT or self.rect.top < 0:
                self.speed_y *= -self.elasticity

            # makes ball stop if not enough energy left for ball
            if self.rect.bottom == SCREEN_HEIGHT and self.speed_y > -5:
                self.is_stopped = True

    def show(self, surface):
        surface.blit(self.image, self.rect)


class Player(pygame.sprite.Sprite):
    def __init__(self, size=100, *groups):
        super().__init__(*groups)
        # todo implement which side player it is
        player_image = pygame.image.load("player.png")
        self.image = pygame.transform.scale(player_image, (size,) * 2)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(0, SCREEN_HEIGHT - size)
        self.speed_x = 10
        self.speed_y = -10
        self.is_moving_left = False
        self.is_moving_right = False
        self.is_in_jump = False

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
        self.speed_y += GRAVITY
        if self.rect.bottom + self.speed_y >= SCREEN_HEIGHT:
            self.rect = self.rect.move(0, SCREEN_HEIGHT - self.rect.bottom)
            self.is_in_jump = False
            self.speed_y = -10
        self.rect = self.rect.move(0, self.speed_y)

    def make_move(self):
        if self.is_moving_left:
            self.rect = self.rect.move(-self.speed_x, 0)
        if self.is_moving_right:
            self.rect = self.rect.move(self.speed_x, 0)
        if self.is_in_jump:
            self._jump()

    def show(self, surface):
        surface.blit(self.image, self.rect)


clock = pygame.time.Clock()
pygame.init()
all_sprites = pygame.sprite.Group()
ball_sprite = pygame.sprite.Group()
volleyball_ball = Ball(50, all_sprites, ball_sprite)
player = Player(100, all_sprites)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player.move_left_started()
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                player.move_right_started()
            if event.key == pygame.K_UP or event.key == ord('w'):
                player.move_jump()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player.move_left_stopped()
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                player.move_right_stopped()
    volleyball_ball.move()
    display.fill(WHITE)
    volleyball_ball.show(surface=display)
    player.make_move()
    player.show(surface=display)
    collided = pygame.sprite.collide_rect(player, volleyball_ball)
    print(collided) # todo
    pygame.display.flip()
    clock.tick(FPS)
