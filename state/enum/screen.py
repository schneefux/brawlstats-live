from enum import Enum, unique

@unique
class Screen(Enum):
    # corresponds to templates/screen/{name.lower()}.png
    MAIN_MENU = {
        "id": "main_menu",
        "next": (
            "main_menu_team",
            "battle_log",
            "choose_event",
            "queue",
            "chest",
            "brawlers"
        )
    }
    MAIN_MENU_TEAM = {
        "id": "main_menu_team",
        "next": (
            "main_menu",
            "battle_log",
            "choose_event",
            "queue",
            "chest",
            "brawlers"
        )
    }
    BRAWLERS = {
        "id": "brawlers",
        "next": ("select_brawler", "main_menu", "main_menu_team")
    }
    SELECT_BRAWLER = {
        "id": "select_brawler",
        "next": ("brawlers", "main_menu", "main_menu_team")
    }
    CHEST = {
        "id": "chest",
        "next": ("main_menu", "main_menu_team")
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

    @staticmethod
    def get_first():
        return [Screen.MAIN_MENU, Screen.LOADING, Screen.QUEUE]

    def get_next(self):
        return [Screen[n.upper()] for n in self.value["next"]]
