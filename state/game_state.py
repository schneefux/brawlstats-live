from attr import attrs, attrib
from state.enum.screen import Screen
from state.enum.match_result import MatchResult
from state.stream_config import StreamConfig

@attrs(frozen=True)
class GameState(object):
    stream_config = attrib(type=StreamConfig)
    timestamp = attrib(type=int, default=None)
    seconds = attrib(type=float, default=0.0)
    screen = attrib(type=Screen, default=None)
    last_match_result = attrib(type=MatchResult, default=None)
    blue_team = attrib(type=list, default=[])
    red_team = attrib(type=list, default=[])
    blue_gems = attrib(type=int, default=0)
    red_gems = attrib(type=int, default=0)
    taking_damage = attrib(type=bool, default=False)