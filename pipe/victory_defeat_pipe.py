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
        self._matcher.load_templates("templates/victory_defeat/*.png",
                                     1080)

    def process(self, frame, state):
        if state.current_screen != Screen.VICTORY_DEFEAT:
            return {}

        results = self._matcher.classify(frame, state.stream_config,
                                         True)
        if len(results) != 1:
            # misclassified, save screenshot
            filename = "{}_{}.png".format(
                state.stream_config.channel, state.timestamp)
            cv2.imwrite(filename, frame)
            logging.warning(
                "Screen was classified as victory/defeat " +
                "but no result template matched")
            return {}

        result_label, position = results[0]

        changes = {
            "last_match_result": MatchResult(result_label)
        }

        positions = state.stream_config.template_positions.copy()
        positions[result_label] = position
        stream_config = evolve(
            state.stream_config,
            template_positions=positions)
        changes["stream_config"] = stream_config

        return changes
