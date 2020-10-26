from enum import Enum, auto


class States(Enum):
    """State machine constants for the StateMachine class """
    STATE_MENU = auto()
    STATE_PLAY = auto()


class StateMachine:
    """Manages a stack-based state machine.
    peek(), pop() and push() perform as traditionally expected.
    peeking and popping an empty stack returns None,
    """

    def __init__(self):
        self.state_stack = []

    def peek(self):
        """Returns the current state without altering the stack.
        Returns None if the stack is empty
        """
        try:
            return self.state_stack[-1]
        except IndexError:
            return None  # empty stack

    def pop(self):
        """Remove the current state from the stack.
        Return true if there are any states in the stack else False.
        Returns None if the stack is empty.
        """
        try:
            self.state_stack.pop()
        except IndexError:
            return None
        else:
            # returns if there are any states
            # if the game is running there should
            # be always at least 1 state present
            return len(self.state_stack) > 0

    def push(self, state):
        """Push a new state onto the stack.
        Returns the pushed value
        """
        self.state_stack.append(state)
