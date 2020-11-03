import json

from event_manager import TickEvent, InitializeEvent, StateChangeEvent, QuitEvent, Listener, KeyboardPressEvent, \
    KeyboardReleaseEvent, Event
from models.game_state import GameState
from models.state_machine import StateMachine, States
from network import Network
from views.menu import GameModes


def encode_event(event: Event):
    data = {"event": str(event), "data": None}
    if isinstance(event, (KeyboardReleaseEvent, KeyboardPressEvent)):
        data["data"] = event.key
    return json.dumps(data).encode()


def decode_event(event_str: str):
    event_data = json.loads(event_str)
    return event_data["event"], event_data["data"]


class GameEngine(Listener):
    """
    Tracks the game state
    """

    def __init__(self, event_manager):
        """
        @param event_manager: Pointer to EventManager allows us to post messages to the event queue
        """
        super().__init__(event_manager)  # Register listener to event manager
        # True while the engine is online. Changed via QuitEvent()
        self.running = False
        self.game_mode = None
        self.state = StateMachine()
        self.game_state = GameState()
        self.game_state.setup_pre_game(is_left_side_starts=True)
        self.connection = Network(event_manager=self.event_manager, game_engine=self)

    def notify(self, event):
        """Called by an event in the message queue."""
        if isinstance(event, QuitEvent):
            self.running = False
        if isinstance(event, StateChangeEvent):
            if event.state:
                # push a new state on the stack
                self.state.push(event.state)
                return

            # pop request
            # false if no more states are left
            if not self.state.pop():
                self.event_manager.post(QuitEvent())

        if self.game_mode == GameModes.MULTI_PLAYER_ONLINE:
            encoded_event = encode_event(event)
            self.connection.send(encoded_event)

        elif isinstance(event, KeyboardPressEvent) and self.game_mode == GameModes.MULTI_PLAYER_LOCAL:
            self.game_state.handle_start_move_event(key=event.key)
        elif isinstance(event, KeyboardReleaseEvent) and self.game_mode == GameModes.MULTI_PLAYER_LOCAL:
            self.game_state.handle_end_move_event(key=event.key)
        elif isinstance(event, TickEvent) and self.game_mode == GameModes.MULTI_PLAYER_LOCAL:
            self.game_state.handle_game_tick_event()

    def run(self):
        """Starts the game engine loop.
        This pumps a Tick event into the message queue for each loop.
        The loop ends when this object hears a QuitEvent in notify()
        """
        self.running = True



        self.event_manager.post(InitializeEvent())
        # we push our first state to the stack
        # our menu is always the first game state
        # the game always starts from the main menu
        self.state.push(States.STATE_MENU)
        while self.running:
            new_tick = TickEvent()
            self.event_manager.post(new_tick)

            if self.state.peek() == States.STATE_PLAY and self.game_mode == GameModes.MULTI_PLAYER_LOCAL:
                self.game_state.check_game_rules_violation()
                self.game_state.calculate_points_and_start_new_match()

            elif self.state.peek() == States.STATE_PLAY and self.game_mode == GameModes.MULTI_PLAYER_ONLINE and self.connection.game_info:
                game_info = self.connection.game_info

                self.game_state.player1.rect.x = game_info["player1_x"]
                self.game_state.player1.rect.y = game_info["player1_y"]
                self.game_state.player1.points = game_info["player1_points"]
                self.game_state.player2.rect.x = game_info["player2_x"]
                self.game_state.player2.rect.y = game_info["player2_y"]
                self.game_state.player2.points = game_info["player2_points"]
                self.game_state.ball.rect.x = game_info["ball_x"]
                self.game_state.ball.rect.y = game_info["ball_y"]
