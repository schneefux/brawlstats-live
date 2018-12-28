from attr import attrs, attrib
from state.screen import Screen
from state.match_result import MatchResult
from state.stream_config import StreamConfig

@attrs(frozen=True)
class GameState(object):
    stream_config = attrib(type=StreamConfig)
    current_screen = attrib(type=Screen, default=None)
    last_known_screen = attrib(type=Screen, default=None)
    last_match_result = attrib(type=MatchResult, default=None)
    timestamp = attrib(type=int, default=None)
    blue_team = attrib(type=list, default=[])
    red_team = attrib(type=list, default=[])
