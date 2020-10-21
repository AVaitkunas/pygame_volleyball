import sys
import pygame

# SETTINGS
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

WHITE = (225,) * 3
BLACK = (0,) * 3

display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
display.fill(WHITE)
pygame.display.set_caption("Volleyball")


class Ball:
    def __init__(self, diameter=50):
        self.speed_x = 10
        self.speed_y = 0
        self.gravity = 1
        self.is_stopped = False
        ball_image = pygame.image.load("ball.png")
        self.image = pygame.transform.scale(ball_image, (diameter,) * 2)
        self.ball_rect = self.image.get_rect()
        self.elasticity = 0.8

    def move(self):
        """Makes ball move. Gravity is taken into account."""
        if not self.is_stopped:
            self.speed_y += self.gravity
            # handling of ball appearing bellow screen boundaries
            if self.ball_rect.bottom + self.speed_y < SCREEN_HEIGHT:
                self.ball_rect = self.ball_rect.move(self.speed_x, self.speed_y)
            else:
                self.ball_rect = self.ball_rect.move(self.speed_x, SCREEN_HEIGHT - self.ball_rect.bottom)

            # handling of ball bounces from walls
            if self.ball_rect.right >= SCREEN_WIDTH or self.ball_rect.left < 0:
                self.speed_x *= -self.elasticity
            if self.ball_rect.bottom >= SCREEN_HEIGHT or self.ball_rect.top < 0:
                self.speed_y *= -self.elasticity

            # makes ball stop if not enough energy left for ball
            if self.ball_rect.bottom == SCREEN_HEIGHT and self.speed_y > -5:
                self.is_stopped = True

    def show(self, surface):
        surface.blit(self.image, self.ball_rect)


pygame.init()
volleyball_ball = Ball()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.time.delay(50)
    volleyball_ball.move()
    display.fill(WHITE)
    volleyball_ball.show(surface=display)
    pygame.display.update()
