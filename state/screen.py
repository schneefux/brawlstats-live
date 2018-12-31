from enum import Enum, unique

@unique
class Screen(Enum):
    # corresponds to templates/screen/{name.lower()}.png
    MAIN_MENU = {
        "id": "main_menu",
        "next": ("main_menu_team", "battle_log", "choose_event", "queue")
    }
    MAIN_MENU_TEAM = {
        "id": "main_menu_team",
        "next": ("main_menu", "battle_log", "choose_event", "queue")
    }
    BATTLE_LOG = {
        "id": "battle_log",
        "next": ("main_menu", "main_menu_team")
    }
    CHOOSE_EVENT = {
        "id": "choose_event",
        "next": ("main_menu", "main_menu_team")
    }
    QUEUE = {
        "id": "queue",
        "next": ("loading", )
    }
    LOADING = {
        "id": "loading",
        "next": ("main_menu", "main_menu_team", "versus")
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
