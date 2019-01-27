from enum import Enum, unique

@unique
class Screen(Enum):
    # these are the model/screen/train.py indices
    # = dataset/train/* folder names in alphabetical order
    BATTLE_LOG = 0
    BOUNTY_INGAME = 1
    BRAWLBALL_INGAME = 2
    BRAWLBALL_START = 3
    BRAWLERS = 4
    CHAT = 5
    CHEST = 6
    CHOOSE_EVENT = 7
    DEFEAT = 8
    GEMGRAB_INGAME = 9
    GEMGRAB_START = 10
    HEIST_INGAME = 11
    HEIST_START = 12
    LOADING = 13
    MAIN_MENU = 14
    PLAY_AGAIN = 15
    PROFILE = 16
    QUEUE = 17
    RANK_DUO = 18
    RANK_SOLO = 19
    SELECT_BRAWLER = 20
    SHOWDOWN_DUO_START = 21
    SHOWDOWN_INGAME = 22
    SHOWDOWN_SOLO_START = 23
    VERSUS = 24
    VICTORY = 25
