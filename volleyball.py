import sys
import pygame

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

WHITE = (255,) * 3
BLACK = (0,) * 3

display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
display.fill(WHITE)
pygame.display.set_caption("Volleyball")


class Ball:
    def __init__(self, radius=10):
        self.radius = radius
        self.x = 10
        self.y = 10
        # velocity, vector, acceleration, acc. vector., mass todo write motion equation
        self.speed_x = 1
        self.speed_y = 1

    def move(self):
        # bounce from the walls
        if self.x > SCREEN_WIDTH or self.x < 0:
            self.speed_x *= -1
        if self.y > SCREEN_HEIGHT or self.y < 0:
            self.speed_y *= -1

        self.x += self.speed_x
        self.y += self.speed_y

    def show(self, surface):
        pygame.draw.circle(surface, BLACK, (self.x, self.y), self.radius)


pygame.init()
ball = Ball()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.time.delay(10)
    ball.move()
    display.fill(WHITE)
    ball.show(surface=display)
    pygame.display.update()

