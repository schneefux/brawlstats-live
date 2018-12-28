from enum import Enum, unique

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
