from enum import Enum
from attr import attrs, attrib
from state.stream_config import StreamConfig

class Screen(Enum):
    """
    Screens in the order they appear.
    """
    MAIN_MENU      = 0
    LOADING_VERSUS = 1
    INGAME         = 2
    VICTORY_DEFEAT = 3
    PLAY_AGAIN     = 4


class MatchResult(Enum):
    VICTORY  = "victory"
    DEFEAT   = "defeat"
    RANK_X   = "rank"
    RANK_TOP = "rank_top"


class Brawler(Enum):
    BARLEY   = "barley"
    BROCK    = "brock"
    COLT     = "colt"
    EL_PRIMO = "el_primo"
    JESSIE   = "jessie"
    NITA     = "nita"
    PENNY    = "penny"
    POCO     = "poco"
    RICOCHET = "ricochet"
    SHELLY   = "shelly"


@attrs(frozen=True)
class GameState(object):
    stream_config = attrib(type=StreamConfig)
    current_screen = attrib(type=Screen, default=None)
    last_known_screen = attrib(type=Screen, default=None)
    last_match_result = attrib(type=MatchResult, default=None)
    timestamp = attrib(type=int, default=None)
    blue_team = attrib(type=list, default=[])
    red_team = attrib(type=list, default=[])
