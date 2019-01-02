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

        changes = {
            "current_screen": None
        }
        position = None

        next_screens = []
        if state.last_known_screen is None:
            # if context is completely unknown,
            # check for match start screens
            next_screens = Screen.get_first()
        else:
            # else check if it's one of the next screens
            # or one of the ones after
            current_screens = [state.current_screen]\
                if state.current_screen is not None else []
            next1_screens = state.last_known_screen.get_next()
            next2_screens = [screen
                             for next_screen in next_screens
                             for screen in next_screen.get_next()]
            next_screens = list(set(
                current_screens + next1_screens + next2_screens))

        for next_screen in next_screens:
            matches = self._matchers[next_screen]\
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
