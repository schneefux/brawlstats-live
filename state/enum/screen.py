from enum import Enum, unique

@unique
class Screen(Enum):
    # these are the model/screen/train.py indices
    # = dataset/train/* folder names in alphabetical order
    BATTLE_LOG = 0
    BRAWLERS = 1
    CHEST = 2
    CHOOSE_EVENT = 3
    CLUB = 4
    DEFEAT = 5
    EVENT_INFO = 6
    GEMGRAB_END = 7
    GEMGRAB_INGAME = 8
    GEMGRAB_START = 9
    GEMGRAB_WAIT_RESPAWN = 10
    HEIST_END = 11
    HEIST_INGAME = 12
    HEIST_START = 13
    HEIST_WAIT_RESPAWN = 14
    INVITE = 15
    LOADING = 16
    MAIN_MENU = 17
    MAIN_MENU_TEAM = 18
    PLAY_AGAIN = 19
    PROFILE = 20
    QUEUE = 21
    RANK = 22
    SELECT_BRAWLER = 23
    SHOWDOWN_DEFEATED = 24
    SHOWDOWN_DUO_START = 25
    SHOWDOWN_INGAME = 26
    SHOWDOWN_SHOWDOWN = 27
    SHOWDOWN_SOLO_START = 28
    SHOWDOWN_WAIT_ALLY_RESPAWN = 29
    SHOWDOWN_WAIT_RESPAWN = 30
    TROPHYROAD = 31
    VERSUS = 32
    VICTORY = 33
