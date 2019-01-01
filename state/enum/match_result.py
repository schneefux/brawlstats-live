from enum import Enum, unique

@unique
class MatchResult(Enum):
    VICTORY  = "victory"
    DEFEAT   = "defeat"
    RANK_X   = "rank"
    RANK_TOP = "rank_top"
