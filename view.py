from typing import Tuple

import pygame

from event_manager import Listener, EventManager, InitializeEvent, QuitEvent, TickEvent, StateChangeEvent
from game_engine import GameEngine, States
from views.ball_view import BallView
from views.menu import Menu, MenuActions, GameModes
from views.net_view import NetView
from views.player_view import PlayerView


class GraphicalView(Listener):
    """Draws the models state onto the screen"""

    def __init__(
            self,
            event_manager: EventManager,
            model_object: GameEngine,
            win_size: Tuple[int, int] = (640, 480),
            win_title: str = "VolleyBall",
            fps: int = 30,
    ):
        """
        @param event_manager: Pointer to EventManager allows us to post messages to the event queue
        @param model_object: Pointer to GameEngine: a strong reference to the game Model
        @param win_size: Tuple containing window wight and height
        @param win_title: Window title text
        @param fps: Frames per second
        """
        super().__init__(event_manager)  # Register listener to event manager
        self.event_manager = event_manager
        self.model = model_object
        self.window_size = win_size
        self.window_title = win_title
        self.fps = fps

        self.initialized = False

        self.screen = None  # the screen surface
        self.clock: pygame.time.Clock = None  # keeps the fps constant
        self.small_font = None  # small font

        self.menu = None
        self.player_view = None
        self.ball_view = None
        self.net_view = None

    def notify(self, event):
        """Receive events posted to the message queue"""

        if isinstance(event, InitializeEvent):
            self.initialize()
        elif isinstance(event, QuitEvent):
            # shut down the pygame graphics
            self.initialized = False
            pygame.quit()
        elif isinstance(event, TickEvent):
            # only draw on tick events and when initialized
            if not self.initialized:
                return

            current_state = self.model.state.peek()
            if current_state == States.STATE_MENU:
                if self.render_menu():
                    return
            elif current_state == States.STATE_PLAY:
                self.render_play()

            pygame.display.flip()
            # limit the redraw speed to 30 frames per second
            self.clock.tick(self.fps)

    def render_menu(self):
        """Render the game menu"""
        self.screen.fill(pygame.Color("white"))
        self.menu.game_menu.enable()
        self.menu.show_menu()

        if self.menu.action == MenuActions.QUIT:
            self.event_manager.post(QuitEvent())
            return True
        elif self.menu.action == MenuActions.PLAY:
            self.model.game_mode = self.menu.game_mode
            self.event_manager.post(StateChangeEvent(States.STATE_PLAY))

        return None

    def render_play(self):
        """Render the game play."""
        self.screen.fill(pygame.Color("white"))

        for player in (self.model.game_state.player1, self.model.game_state.player2):
            self.player_view.render_player(
                destination_rect=player.rect,
                is_side_left=player.is_side_left,
                points=player.points
            )

        self.ball_view.render(
            destination_rect=self.model.game_state.ball.rect
        )
        self.net_view.render(
            destination_rect=self.model.game_state.net.rect
        )

    def initialize(self):
        """Set up the pygame graphical display and loads graphical resources"""
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption(self.window_title)
        self.screen = pygame.display.set_mode(self.window_size)
        self.clock = pygame.time.Clock()
        self.small_font = pygame.font.SysFont('Comic Sans MS', 30)
        self.initialized = True

        # todo these guys have to leave this place and go to initialization of game
        self.player_view = PlayerView(surface=self.screen, font=self.small_font)
        self.ball_view = BallView(surface=self.screen)
        self.net_view = NetView(surface=self.screen)
        self.menu = Menu(screen=self.screen)
