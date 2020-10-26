import event_manager as eventmanager
import game_engine
import view
import controller


def run():
    event_manager = eventmanager.EventManager()
    game_model = game_engine.GameEngine(event_manager)
    _keyboard = controller.KeyboardController(event_manager, game_model)
    _graphics = view.GraphicalView(event_manager, game_model)
    game_model.run()


if __name__ == "__main__":
    run()
