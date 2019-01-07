from enum import Enum, unique

@unique
class Screen(Enum):
    # these are the model/screen/train.py indices
    # = dataset/train/* folder names in alphabetical order
    BATTLE_LOG = 0
    BRAWLERS = 1
    CHEST = 2
    CHOOSE_EVENT = 3
    DEFEAT = 4
    LOADING = 5
    MAIN_MENU = 6
    MAIN_MENU_TEAM = 7
    MODE_GEM_GRAB = 8
    MODEL_SOLO_SHOWDOWN = 9
    PLAY_AGAIN = 10
    QUEUE = 11
    RANK = 12
    VERSUS = 13
    VICTORY = 14
