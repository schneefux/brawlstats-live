from enum import Enum
from attr import attrs, attrib
from state.stream_config import StreamConfig

class Screen(Enum):
    MAIN_MENU      = "main_menu"
    LOADING_VERSUS = "versus"
    INGAME         = "ingame"
    VICTORY_DEFEAT = "post_match"
    PLAY_AGAIN     = "play_again"

@attrs(frozen=True)
class GameState(object):
    stream_config = attrib(type=StreamConfig)
    screen = attrib(type=Screen)
