from enum import Enum, unique

@unique
class Screen(Enum):
    # these are the model/screen/train.py indices
    # = dataset/train/* folder names in alphabetical order
    BATTLE_LOG = 0
    BOUNTY_INGAME = 1
    BRAWLBALL_INGAME = 2
    BRAWLERS = 3
    CHAT = 4
    CHOOSE_EVENT = 5
    DEFEAT = 6
    GEMGRAB_INGAME = 7
    GEMGRAB_START = 8
    GEMGRAB_VERSUS = 9
    GEMGRAB_WAIT_RESPAWN = 10
    HEIST_INGAME = 11
    LOADING = 12
    MAIN_MENU = 13
    MAIN_MENU_TEAM = 14
    PLAY_AGAIN = 15
    QUEUE = 16
    RANK_DUO = 17
    RANK_SOLO = 18
    SELECT_BRAWLER = 19
    SHOWDOWN_BRAWL = 20
    SHOWDOWN_DUO_START = 21
    SHOWDOWN_INGAME = 22
    SHOWDOWN_SOLO_START = 23
    SHOWDOWN_WAIT_RESPAWN = 24
    VICTORY = 25
