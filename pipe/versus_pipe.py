import cv2
import logging

from pipe.pipe import Pipe
from state.game_state import Screen, Brawler
from classifiers.template_matcher import TemplateMatcher

class VersusPipe(Pipe):
    """
    Extract information from the versus screen.
    """
    realtime = False

    def __init__(self):
        self._matcher = TemplateMatcher()

    def start(self):
        self._matcher.load_templates("templates/brawler/*.png",
                                     1080)

    def process(self, frame, state):
        if state.current_screen != Screen.VERSUS or \
                state.stream_config.screen_box is None:
            return {}

        matches = self._matcher.classify(frame,
                                         state.stream_config)
        if len(matches) == 0:
            # misclassified, save screenshot
            filename = "{}_{}.png".format(
                state.stream_config.channel, state.timestamp)
            cv2.imwrite(filename, frame)
            logging.warning(
                "Screen was classified as versus " +
                "but no brawler template matched")
            return {}

        screen_box = state.stream_config.screen_box
        average_y = (screen_box[1][1] - screen_box[0][1]) / 2
        blue_team = [Brawler(match[0]) for match in matches
                     if match[1][0] > average_y]
        red_team = [Brawler(match[0]) for match in matches
                     if match[1][0] < average_y]

        return {
            "red_team": red_team,
            "blue_team": blue_team
        }
