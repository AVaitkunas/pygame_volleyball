import pygame_menu
from settings import SCREEN_WIDTH, SCREEN_HEIGHT


class Menu:
    def __init__(self, screen):
        self.game_menu = pygame_menu.Menu(
            width=SCREEN_WIDTH,
            height=SCREEN_HEIGHT,
            title="VolleyBall Game Menu",
            theme=pygame_menu.themes.THEME_DARK
        )
        self.screen = screen
        self.game_mode = None

        # todo does not do anything yet. think how to apply for multiplayer
        self.game_menu.add_text_input(
            title="Nickname: ",
            default="Curly",
            onchange=self.set_player_name
        )
        self.game_menu.add_selector(
            "Select Game Mode: ",
            [(" Multi-player 1 PC ", 1), ("Multi-player Online", 2), ("   Single-player   ", 3)],
            onchange=self.set_game_mode,
            default=0
        )

        self.game_menu.add_button('Play', self.start_game)
        self.game_menu.add_button('Quit', self.quit)

    def show_menu(self):
        self.game_menu.mainloop(surface=self.screen)

    def set_player_name(self, name):
        print(f"set player name to {name}")

    def set_game_mode(self, value, game_mode):
        print(f"{value} and {game_mode}")

    def start_game(self):
        print("start game")

    def settings(self):
        print("settings page")

    def quit(self):
        print("quit the game")
