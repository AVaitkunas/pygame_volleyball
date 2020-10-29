from enum import Enum, auto

import pygame_menu
from settings import SCREEN_WIDTH, SCREEN_HEIGHT


class MenuActions(Enum):
    PLAY = auto()
    SETTINGS = auto()
    QUIT = auto()


class GameModes(Enum):
    MULTI_PLAYER_LOCAL = auto()
    MULTI_PLAYER_ONLINE = auto()
    SINGLE_PLAYER = auto()


class Menu:
    def __init__(self, screen):
        self.game_menu = pygame_menu.Menu(
            width=SCREEN_WIDTH,
            height=SCREEN_HEIGHT,
            title="VolleyBall Game Menu",
            theme=pygame_menu.themes.THEME_DARK
        )
        self.screen = screen
        self.game_mode = GameModes.MULTI_PLAYER_LOCAL

        # todo does not do anything yet. think how to apply for multiplayer
        self.game_menu.add_text_input(
            title="Nickname: ",
            default="Curly",
            onchange=self.set_player_name
        )
        self.game_menu.add_selector(
            "Select Game Mode: ",
            [(" Multi-player 1 PC ", GameModes.MULTI_PLAYER_LOCAL),
             ("Multi-player Online", GameModes.MULTI_PLAYER_ONLINE),
             ("   Single-player   ", GameModes.SINGLE_PLAYER)],
            onchange=self.set_game_mode,
        )
        self.action = None
        self.game_menu.add_button('Play', self.start_game)
        self.game_menu.add_button('Quit', self.quit)

    def show_menu(self):
        self.game_menu.mainloop(surface=self.screen, disable_loop=True)

    def set_player_name(self, name):
        print(f"set player name to {name}")

    def set_game_mode(self, _, game_mode):
        self.game_mode = game_mode

    def start_game(self):
        self.action = MenuActions.PLAY
        self.game_menu.disable()

    def settings(self):
        self.action = MenuActions.SETTINGS
        self.game_menu.disable()

    def quit(self):
        self.action = MenuActions.QUIT
        self.game_menu.disable()
