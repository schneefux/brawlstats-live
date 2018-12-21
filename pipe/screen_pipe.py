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
        self._matcher = TemplateMatcher()

    def start(self):
        self._matcher.load_templates("templates/screen/*.png",
                                     1080, True)

    def process(self, frame, state):
        screen_label, stream_config = self._matcher.classify(
            frame, state.stream_config)

        if state.screen == Screen.VICTORY_DEFEAT \
                and screen_label is None:
            screen_label = Screen.PLAY_AGAIN

        if screen_label is None:
            return {
                "stream_config": stream_config
            }

        return {
            "screen": Screen(screen_label),
            "stream_config": stream_config
        }
