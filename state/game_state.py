from enum import Enum
from attr import attrs, attrib
from state.stream_config import StreamConfig

class Screen(Enum):
    MAIN_MENU      = "main_menu"
    LOADING_VERSUS = "versus"
    INGAME         = "ingame"
    VICTORY_DEFEAT = "post_match"
    PLAY_AGAIN     = "play_again"

class MatchResult(Enum):
    VICTORY  = "victory"
    DEFEAT   = "defeat"
    RANK_X   = "rank"
    RANK_TOP = "rank_top"

@attrs(frozen=True)
class GameState(object):
    stream_config = attrib(type=StreamConfig)
    screen = attrib(type=Screen)
    last_match_result = attrib(type=MatchResult, default=None)
    timestamp = attrib(type=int, default=None)
    last_frame_processed_timestamp = attrib(type=int, default=None)
