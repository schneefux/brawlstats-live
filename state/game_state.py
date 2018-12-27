from enum import Enum, unique
from attr import attrs, attrib
from state.stream_config import StreamConfig

@unique
class Screen(Enum):
    # corresponds to templates/screen/{name.lower()}.png
    MAIN_MENU = {
        "id": "main_menu",
        "next": ("battle_log", "choose_event", "queue")
    }
    BATTLE_LOG = {
        "id": "battle_log",
        "next": ("main_menu", )
    }
    CHOOSE_EVENT = {
        "id": "choose_event",
        "next": ("main_menu", )
    }
    QUEUE = {
        "id": "queue",
        "next": ("loading", )
    }
    LOADING = {
        "id": "loading",
        "next": ("main_menu", "versus")
    }
    VERSUS = {
        "id": "versus",
        "next": ("victory_defeat", )
    }
    VICTORY_DEFEAT = {
        "id": "victory_defeat",
        "next": ("play_again", )
    }
    PLAY_AGAIN = {
        "id": "play_again",
        "next": ("queue", "loading")
    }

    def get_next(self):
        return [Screen[n.upper()] for n in self.value["next"]]

@unique
class MatchResult(Enum):
    VICTORY  = "victory"
    DEFEAT   = "defeat"
    RANK_X   = "rank"
    RANK_TOP = "rank_top"


@unique
class Brawler(Enum):
    BARLEY   = "barley"
    BO       = "bo"
    BROCK    = "brock"
    BULL     = "bull"
    COLT     = "colt"
    CROW     = "crow"
    DARRYL   = "darryl"
    DYNAMIKE = "dynamike"
    EL_PRIMO = "el_primo"
    FRANK    = "frank"
    JESSIE   = "jessie"
    LEON     = "leon"
    MORTIS   = "mortis"
    NITA     = "nita"
    PAM      = "pam"
    PENNY    = "penny"
    PIPER    = "piper"
    POCO     = "poco"
    RICOCHET = "ricochet"
    SHELLY   = "shelly"
    SPIKE    = "spike"
    TARA     = "tara"
    BOSS_ROBOT = "boss_robot"


@attrs(frozen=True)
class GameState(object):
    stream_config = attrib(type=StreamConfig)
    current_screen = attrib(type=Screen, default=None)
    last_known_screen = attrib(type=Screen, default=None)
    last_match_result = attrib(type=MatchResult, default=None)
    timestamp = attrib(type=int, default=None)
    blue_team = attrib(type=list, default=[])
    red_team = attrib(type=list, default=[])
