from event_manager import TickEvent, InitializeEvent, StateChangeEvent, QuitEvent, Listener, KeyboardPressEvent, \
    KeyboardReleaseEvent
from models.game_state import GameState
from models.state_machine import StateMachine, States


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
        if isinstance(event, KeyboardPressEvent):
            # connection.send(event)
            self.game_state.handle_start_move_event(event=event)
        if isinstance(event, KeyboardReleaseEvent):
            self.game_state.handle_end_move_event(event=event)
        if isinstance(event, TickEvent):
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

            if self.state.peek() == States.STATE_PLAY:
                self.game_state.check_game_rules_violation()
                self.game_state.calculate_points_and_start_new_match()

            # if opponent_connected:
            #     new_data= connection.read()
            #     self.game_state.player1.rect = new_data.player1.rect
