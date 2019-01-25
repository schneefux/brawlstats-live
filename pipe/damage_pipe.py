from pipe.pipe import Pipe
from state.enum.screen import Screen
from matcher.damage_matcher import DamageMatcher

class DamagePipe(Pipe):
    def __init__(self):
        self._matcher = DamageMatcher()

    def process(self, frame, state):
        if state.stream_config.screen_box is None:
            return {}

        matches = self._matcher.classify(frame,
            state.stream_config)

        if matches != state.taking_damage:
            return {
                "taking_damage": matches
            }
        else:
            return {}