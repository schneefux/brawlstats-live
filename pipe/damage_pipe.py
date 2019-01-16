from pipe.pipe import Pipe
from state.enum.screen import Screen
from classifiers.color_matcher import ColorMatcher, ColorRange

class DamagePipe(Pipe):
    def __init__(self):
        self._matcher = ColorMatcher(ColorRange.DAMAGE())

    def process(self, frame, state):
        if state.stream_config.screen_box is None:
            return {}

        matches = self._matcher.classify(frame, state.stream_config)[0]
        return {
            "taking_damage": matches
        }
