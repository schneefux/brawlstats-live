import cv2
import logging
from attr import evolve

from pipe.pipe import Pipe
from state.game_state import MatchResult, Screen
from classifiers.template_matcher import TemplateMatcher

class VictoryDefeatPipe(Pipe):
    """
    Extract information from the victory/defeat screen.
    """
    realtime = False

    def __init__(self):
        self._matcher = TemplateMatcher()

    def start(self):
        self._matcher.load_templates("templates/post_match/*.png",
                                     1080, True)

    def process(self, frame, state):
        if state.current_screen != Screen.VICTORY_DEFEAT:
            return {}

        result_label = self._matcher.classify(frame,
                                              state.stream_config)[0]
        if result_label is None:
            # misclassified, save screenshot
            filename = "{}_{}.png".format(
                state.stream_config.channel, state.timestamp)
            cv2.imwrite(filename, frame)
            logging.warning(
                "Screen was classified as victory/defeat " +
                "but no result template matched")
            return {}

        return {
            "last_match_result": MatchResult(result_label)
        }
