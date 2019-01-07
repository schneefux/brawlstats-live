from attr import attrs, attrib
from state.enum.screen import Screen
from state.enum.match_result import MatchResult
from state.stream_config import StreamConfig

@attrs(frozen=True)
class GameState(object):
    stream_config = attrib(type=StreamConfig)
    screen = attrib(type=Screen, default=None)
    last_match_result = attrib(type=MatchResult, default=None)
    timestamp = attrib(type=int, default=None)
    blue_team = attrib(type=list, default=[])
    red_team = attrib(type=list, default=[])
