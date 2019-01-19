from pipe.pipe import Pipe
from state.enum.screen import Screen
from matcher.gembar_matcher import BlueGembarMatcher, RedGembarMatcher

class GembarPipe(Pipe):
    def __init__(self):
        self._matcher_blue = BlueGembarMatcher()
        self._matcher_red = RedGembarMatcher()

    def process(self, frame, state):
        if state.stream_config.screen_box is None:
            return {}
        if state.screen == Screen.PLAY_AGAIN:
            return {
                "blue_gems": 0,
                "red_gems": 0,
            }
        if state.screen != Screen.GEMGRAB_INGAME:
            return {}

        blue_ratio = self._matcher_blue.classify(
            frame, state.stream_config)
        red_ratio = self._matcher_red.classify(
            frame, state.stream_config)
        
        changes = {}
        if blue_ratio is not None:
            changes["blue_gems"] = round(10*blue_ratio)
        if red_ratio is not None:
            changes["red_gems"] = round(10*red_ratio)

        return changes
