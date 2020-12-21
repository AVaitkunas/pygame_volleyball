import pygame

from event_manager import Listener, TickEvent, QuitEvent, StateChangeEvent, KeyboardPressEvent, KeyboardReleaseEvent, \
    PauseEvent
from game_engine import States


class KeyboardController(Listener):
    """Handles keyboard input"""

    def __init__(self, event_manager, model_object):
        """
        @param event_manager: Pointer to EventManager allows us to post messages to the event queue
        @param model_object: Pointer to GameEngine: a strong reference to the game Model
        """
        # Register listener to event manager
        super().__init__(event_manager)
        self.model = model_object

        self.key_events_map = {
            # todo are menu key presses makes sense anymore?
            States.STATE_MENU: {"press": self.key_down_events_menu, "release": None},
            States.STATE_PLAY: {"press": self.key_down_events_play, "release": self.key_up_events_play},
        }

    def notify(self, event):
        """Receives events posted to the message queue"""
        if not isinstance(event, TickEvent):
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.event_manager.post(QuitEvent())
            if event.type == pygame.KEYDOWN:
                self.handle_key_down_event(event)
            if event.type == pygame.KEYUP:
                self.handle_key_up_event(event)

    def handle_key_down_event(self, event):

        if event.key == pygame.K_ESCAPE:
            self.event_manager.post(StateChangeEvent(None))
            return

        current_state = self.model.state.peek()

        handlers = self.key_events_map.get(current_state)
        if handlers is None or "press" not in handlers:
            raise Exception(
                f"Unknown state: {current_state}. No handling defined for state."
            )
        if handlers["press"] is not None:
            handlers["press"](event)

    def handle_key_up_event(self, event):

        current_state = self.model.state.peek()
        handlers = self.key_events_map.get(current_state)

        if handlers is None or "release" not in handlers:
            raise Exception(f"Unknown state: {current_state}. No handling defined for state.")
        if handlers["release"] is not None:
            handlers["release"](event)

    def key_down_events_menu(self, event):
        """Handles all key event in game state MENU."""

        # escape pops the menu todo not working anymore
        if event.key == pygame.K_ESCAPE:
            self.event_manager.post(StateChangeEvent(None))

        # space plays the game
        if event.key == pygame.K_SPACE:
            self.event_manager.post(StateChangeEvent(States.STATE_PLAY))

    def key_down_events_play(self, event):
        """Handles play key events"""
        if event.key == pygame.K_ESCAPE:
            self.event_manager.post(StateChangeEvent(None))

        if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, ord('a'), ord('d'), ord('w')]:
            self.event_manager.post(KeyboardPressEvent(key=event.key))

        if event.key == ord('p'):
            self.event_manager.post(PauseEvent())

    def key_up_events_play(self, event):
        """Handles play key events"""
        if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, ord('a'), ord('d'), ord('w')]:
            self.event_manager.post(KeyboardReleaseEvent(key=event.key))
