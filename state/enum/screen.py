from enum import Enum, unique

@unique
class Screen(Enum):
    # these are the model/screen/train.py indices
    # = dataset/train/* folder names in alphabetical order
    DEFEAT = 0
    GEMGRAB_INGAME = 1
    GEMGRAB_START = 2
    GEMGRAB_VERSUS = 3
    GEMGRAB_WAIT_RESPAWN = 4
    LOADING = 5
    MAIN_MENU = 6
    PLAY_AGAIN = 7
    QUEUE = 8
    RANK = 9
    SHOWDOWN_DUO_START = 10
    SHOWDOWN_INGAME = 11
    SHOWDOWN_SOLO_START = 12
    SHOWDOWN_WAIT_RESPAWN = 13
    VICTORY = 14
