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
                1080)

    def process(self, frame, state):
        if state.stream_config.screen_box is None:
            return {}

        changes = {}

        # if context is completely unknown,
        # check for match start screens
        if state.last_known_screen is None:
            matchers = [self._matchers[screen] for screen in Screen
                        if Screen.VICTORY_DEFEAT in screen.get_next()]
            for matcher in matchers:
                screen_label, position = matcher.classify(
                    frame, state.stream_config)

                if screen_label is not None:
                    # match
                    screen = Screen[screen_label.upper()]
                    changes = {
                        "current_screen": screen,
                        "last_known_screen": screen
                    }
                    break

        # check if it's the same screen
        elif state.current_screen is not None:
            screen_label, position = \
                self._matchers[state.current_screen]\
                .classify(frame, state.stream_config)

            if screen_label is None:
                # current: unknown, previous = current
                changes = {
                    "current_screen": None,
                    "last_known_screen": state.current_screen
                }
            elif screen_label != state.current_screen.name.lower():
                # match
                screen = Screen[screen_label.upper()]
                changes = {
                    "current_screen": screen,
                    "last_known_screen": screen
                }

        # check if it's one of the next screens
        elif state.last_known_screen is not None:
            for screen in state.last_known_screen.get_next():
                screen_label, position = self._matchers[screen]\
                    .classify(frame, state.stream_config)
                if screen_label is not None:
                    # match
                    screen = Screen[screen_label.upper()]
                    changes = {
                        "current_screen": screen,
                        "last_known_screen": screen
                    }
                    break

        # else: no match, changes = {}

        if position is not None:
            # cache template position
            positions = state.stream_config\
                .template_positions.copy()
            positions[screen_label] = position
            stream_config = evolve(
                state.stream_config,
                template_positions=positions)
            changes["stream_config"] = stream_config

        return changes
