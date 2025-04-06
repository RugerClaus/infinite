
# WINDOW STATES:
# main menu
# options menu
# playing game

# GAME STATES
# playing game
# playing cutscene
# level playing

from enum import Enum, auto

class APPSTATE(Enum):
    MAIN_MENU = auto()
    OPTIONS_MENU = auto()
    PLAYING_GAME = auto()
    PLAYING_CUTSCENE = auto()
    WORLD = auto()
    

class State:
    def __init__(self):
        self.current_state = APPSTATE.MAIN_MENU
        self.previous_state = None
        self.input_locked = False

    def lock_input(self):
        self.input_locked = True

    def unlock_input(self):
        self.input_locked = False

    def set_state(self, new_state):
        self.previous_state = self.current_state
        self.current_state = new_state

    def is_state(self,state):
        return self.current_state == state