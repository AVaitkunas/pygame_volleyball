from enum import Enum, auto

import pygame

from models.static_objects import Wall
from models.ball import Ball
from models.player import Player
from settings import WALL_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH, PLAYER_STRENGTH, PLAYER_1_CONTROLS, PLAYER_2_CONTROLS, \
    NET_HEIGHT, NET_WIDTH


class States(Enum):
    PRE_GAME = auto()
    PLAY = auto()
    GAME_OVER = auto()


class GameState:
    def __init__(self):

        self.player1 = Player(is_side_left=False, controls=PLAYER_1_CONTROLS)
        self.player2 = Player(is_side_left=True, controls=PLAYER_2_CONTROLS)
        self.ball = Ball()

        self.vertical_walls = pygame.sprite.Group()
        self.horizontal_walls = pygame.sprite.Group()

        self.net = Wall(
            self.vertical_walls,
            rect=(int(SCREEN_WIDTH / 2) - NET_WIDTH, SCREEN_HEIGHT - NET_HEIGHT, NET_WIDTH * 2, NET_HEIGHT)
        )
        self.floor = Wall(
            self.horizontal_walls,
            rect=(0, SCREEN_HEIGHT - WALL_WIDTH, SCREEN_WIDTH, WALL_WIDTH)
        )

        Wall(self.vertical_walls, rect=(0, 0, WALL_WIDTH, SCREEN_HEIGHT))
        Wall(self.vertical_walls, rect=(SCREEN_WIDTH - WALL_WIDTH, 0, WALL_WIDTH, SCREEN_HEIGHT))
        Wall(self.horizontal_walls, rect=(0, 0, SCREEN_WIDTH, WALL_WIDTH))

    def clean_up(self):
        for player in (self.player1, self.player2):
            player.won_match = False
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

    def handle_start_move_event_player_1(self, key):
        if key in list(self.player1.controls):
            self.player1.start_move(key=key)

    def handle_start_move_event_player_2(self, key):
        if key in list(self.player2.controls):
            self.player2.start_move(key=key)

    def handle_end_move_event_player_1(self, key):
        if key in list(self.player1.controls):
            self.player1.end_move(key=key)

    def handle_end_move_event_player_2(self, key):
        if key in list(self.player2.controls):
            self.player2.end_move(key=key)

    def handle_start_move_event(self, key):
        self.handle_start_move_event_player_1(key=key)
        self.handle_start_move_event_player_2(key=key)

    def handle_end_move_event(self, key):
        self.handle_end_move_event_player_1(key=key)
        self.handle_end_move_event_player_2(key=key)

    def handle_ball_collision(self):
        if self.player1.rect.colliderect(self.ball.rect):
            self.ball.hit(
                object_rect=self.player1.rect,
                strength=PLAYER_STRENGTH,
                speed_in_y=self.player1.speed_y,
                is_in_jump=self.player1.movement.in_jump
            )

            self.player1.consecutive_hits += 1
            self.player2.consecutive_hits = 0

        if self.player2.rect.colliderect(self.ball.rect):
            self.ball.hit(
                object_rect=self.player2.rect,
                strength=PLAYER_STRENGTH,
                speed_in_y=self.player2.speed_y,
                is_in_jump=self.player2.movement.in_jump
            )
            self.player1.consecutive_hits = 0
            self.player2.consecutive_hits += 1

        if pygame.sprite.spritecollide(self.ball, self.vertical_walls, False):
            self.ball.bounce_x()

        if pygame.sprite.spritecollide(self.ball, self.horizontal_walls, False):
            self.ball.bounce_y()

    def check_game_rules_violation(self):
        for player in (self.player1, self.player2):
            if pygame.sprite.collide_rect(self.ball, self.floor):
                coord_range = (
                    range(int(SCREEN_WIDTH / 2), SCREEN_WIDTH) if player.is_side_left else
                    range(int(SCREEN_WIDTH / 2))
                )
                if self.ball.rect.centerx in coord_range:
                    player.won_match = True

        if self.player1.consecutive_hits > 3:
            self.player2.won_match = True
        if self.player2.consecutive_hits > 3:
            self.player1.won_match = True

    def calculate_points_and_start_new_match(self):
        for player in (self.player1, self.player2):
            if player.won_match:
                player.points += 1
                self.setup_pre_game(player.is_side_left)
