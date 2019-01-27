from attr import evolve

from pipe.pipe import Pipe
from state.enum.screen import Screen
from matcher.convnet_matcher import ConvnetMatcher

from model.screen.config import shape

class ScreenPipe(Pipe):
    """
    Detect the current game view, for example the loading screen.
    """
    def __init__(self):
        self._matcher = ConvnetMatcher(
            image_shape=shape,
            feature_map={screen.value: screen for screen in Screen})

    def start(self):
        self._matcher.load_model("model/screen/model.h5")

    def process(self, frame, state):
        if state.stream_config.screen_box is None:
            return {}

        matches = self._matcher.classify(frame, state.stream_config)
        if len(matches) == 0:
            return {
                "screen": None
            }

        if len(matches) > 0:
            screen = matches[0][0]
            changes = {}
            if screen == Screen.QUEUE:
                changes["last_queue"] = state.timestamp

            if screen != state.screen:
                changes["screen"] = screen

            return changes