from enum import Enum, auto

import pygame

from models.static_objects import Wall, Net
from models.ball import Ball
from models.player import Player
from settings import WALL_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH, PLAYER_STRENGTH, PLAYER_1_CONTROLS, PLAYER_2_CONTROLS


class States(Enum):
    PRE_GAME = auto()
    PLAY = auto()
    GAME_OVER = auto()


class GameState:
    def __init__(self):

        self.player1 = Player(is_side_left=False, controls=PLAYER_1_CONTROLS)
        self.player2 = Player(is_side_left=True, controls=PLAYER_2_CONTROLS)
        self.ball = Ball()
        self.net = Net()

        self.vertical_walls = pygame.sprite.Group()
        self.horizontal_walls = pygame.sprite.Group()
        self.vertical_walls.add(self.net)
        self.floor = Wall(self.horizontal_walls, rect=(0, SCREEN_HEIGHT - WALL_WIDTH, SCREEN_WIDTH, WALL_WIDTH))
        Wall(self.vertical_walls, rect=(0, 0, WALL_WIDTH, SCREEN_HEIGHT))
        Wall(self.vertical_walls, rect=(SCREEN_WIDTH - WALL_WIDTH, 0, WALL_WIDTH, SCREEN_HEIGHT))
        Wall(self.horizontal_walls, rect=(0, 0, SCREEN_WIDTH, WALL_WIDTH))

    def clean_up(self):
        for player in (self.player1, self.player2):
            player.lost_match = False
            player.consecutive_hits = 0

    def setup_pre_game(self, is_left_side_starts):
        self.clean_up()
        position = SCREEN_WIDTH / 4 if is_left_side_starts else SCREEN_WIDTH / 4 * 3
        self.ball = Ball(position=round(position))

    def handle_game_tick_event(self):
        self.handle_ball_collision()
        self.player1.make_move()
        self.player2.make_move()
        self.ball.make_move()

    def handle_start_move_event(self, event):
        for player in (self.player1, self.player2):
            if event.key in list(player.controls):
                player.start_move(event.key)

    def handle_end_move_event(self, event):
        for player in (self.player1, self.player2):
            if event.key in list(player.controls):
                player.end_move(event.key)

    def handle_ball_collision(self):
        if pygame.sprite.collide_rect(self.player1, self.ball):
            self.ball.hit(self.player1.rect, strength=PLAYER_STRENGTH)

            self.player1.consecutive_hits += 1
            self.player2.consecutive_hits = 0

        if pygame.sprite.collide_rect(self.player2, self.ball):
            self.ball.hit(self.player2.rect, strength=PLAYER_STRENGTH)
            self.player2.consecutive_hits += 1
            self.player1.consecutive_hits = 0

        if pygame.sprite.spritecollide(self.ball, self.vertical_walls, False):
            self.ball.bounce_x()

        if pygame.sprite.spritecollide(self.ball, self.horizontal_walls, False):
            self.ball.bounce_y()

    def check_game_rules_violation(self):
        for player in (self.player1, self.player2):
            if pygame.sprite.collide_rect(self.ball, self.floor):
                coord_range = (
                    range(int(SCREEN_WIDTH / 2)) if player.is_side_left else
                    range(int(SCREEN_WIDTH / 2), SCREEN_WIDTH)
                )
                if self.ball.rect.centerx in coord_range:
                    player.lost_match = True
            if player.consecutive_hits > 3:
                player.lost_match = True

    def calculate_points_and_start_new_match(self):
        for player in (self.player1, self.player2):
            if player.lost_match:
                player.points += 1
                self.setup_pre_game(not player.is_side_left)
