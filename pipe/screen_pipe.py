from attr import evolve

from pipe.pipe import Pipe
from state.game_state import Screen
from classifiers.template_matcher import TemplateMatcher

class ScreenPipe(Pipe):
    """
    Detect the current game view, for example the loading screen.
    """
    realtime = True

    def __init__(self):
        self._matchers = dict()
        for screen in Screen:
            self._matchers[screen] = TemplateMatcher()

    def start(self):
        for screen, matcher in self._matchers.items():
            matcher.load_templates(
                "templates/screen/{}.png".format(screen.name.lower()),
                1080, True)

    def process(self, frame, state):
        screen_label = None

        if state.last_known_screen is None:
            # unknown, try to find match start screens
            matchers = [self._matchers[screen] for screen in Screen
                        if Screen.VICTORY_DEFEAT in screen.get_next()]
            for matcher in matchers:
                screen_label, stream_config = matcher.classify(
                    frame, state.stream_config)
                if screen_label is not None:
                    # match
                    screen = Screen[screen_label.upper()]
                    return {
                        "current_screen": screen,
                        "last_known_screen": screen,
                        "stream_config": stream_config
                    }

            # no match
            return {}

        # check if it's the same screen
        if state.current_screen is not None:
            screen_label = \
                self._matchers[state.current_screen]\
                .classify(frame, state.stream_config)[0]

            if screen_label != state.current_screen.name.lower():
                screen = Screen[screen_label.upper()] if screen_label is not None else None
                return {
                    "current_screen": screen,
                    "last_known_screen": state.current_screen
                }

        # check if it's one of the next screens
        if state.last_known_screen is not None:
            for screen in state.last_known_screen.get_next():
                screen_label = self._matchers[screen]\
                    .classify(frame, state.stream_config)[0]
                if screen_label is not None:
                    # match
                    screen = Screen[screen_label.upper()]
                    return {
                        "current_screen": screen,
                        "last_known_screen": screen
                    }

        # no match
        return {}
