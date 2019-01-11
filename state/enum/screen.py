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
    GEMGRAB_BLUE_COUNTDOWN = 7
    GEMGRAB_BRAWL = 8
    GEMGRAB_COUNTDOWN = 9
    GEMGRAB_INGAME = 10
    GEMGRAB_RED_COUNTDOWN = 11
    GEMGRAB_START = 12
    GEMGRAB_TAKE_DAMAGE = 13
    GEMGRAB_VERSUS = 14
    GEMGRAB_WAIT_RESPAWN = 15
    HEIST_INGAME = 16
    LOADING = 17
    MAIN_MENU = 18
    MAIN_MENU_TEAM = 19
    PLAY_AGAIN = 20
    QUEUE = 21
    RANK_DUO = 22
    RANK_SOLO = 23
    SHOWDOWN_BRAWL = 24
    SHOWDOWN_DEFEATED = 25
    SHOWDOWN_DUO_START = 26
    SHOWDOWN_INGAME = 27
    SHOWDOWN_SHOWDOWN = 28
    SHOWDOWN_SOLO_START = 29
    SHOWDOWN_WAIT_RESPAWN = 30
    VICTORY = 31
