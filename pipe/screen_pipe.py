from attr import evolve

from pipe.pipe import Pipe
from state.enum.screen import Screen
from classifiers.template_matcher import TemplateMatcher

class ScreenPipe(Pipe):
    """
    Detect the current game view, for example the loading screen.
    """
    def __init__(self):
        self._matchers = dict()
        for screen in Screen:
            self._matchers[screen] = TemplateMatcher()

    def start(self):
        for screen, matcher in self._matchers.items():
            matcher.load_templates(
                "templates/screen/{}.png".format(screen.name.lower()),
                1920, 1080)

    def process(self, frame, state):
        if state.stream_config.screen_box is None:
            return {}

        changes = {}
        position = None

        # if context is completely unknown,
        # check for match start screens
        if state.last_known_screen is None:
            matchers = [self._matchers[screen] for screen in [
                Screen.MAIN_MENU, Screen.LOADING, Screen.QUEUE
            ]]
            for matcher in matchers:
                matches = matcher.classify(
                    frame, state.stream_config, True)

                if len(matches) > 0:
                    # match
                    screen_label, position = matches[0]
                    screen = Screen[screen_label.upper()]
                    changes = {
                        "current_screen": screen,
                        "last_known_screen": screen
                    }
                    break

        # check if it's the same screen
        elif state.current_screen is not None:
            matches = self._matchers[state.current_screen]\
                .classify(frame, state.stream_config, True)

            if len(matches) == 0:
                # current: unknown, previous = current
                changes = {
                    "current_screen": None,
                    "last_known_screen": state.current_screen
                }
            # else it must still be the same

        # check if it's one of the next screens
        # or one of the ones after
        elif state.last_known_screen is not None:
            next_screens = state.last_known_screen.get_next()
            next2_screens = [screen
                             for next_screen in next_screens
                             for screen in next_screen.get_next()]
            for screen in set(next_screens + next2_screens):
                matches = self._matchers[screen]\
                    .classify(frame, state.stream_config, True)
                if len(matches) > 0:
                    # match
                    screen_label, position = matches[0]
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
