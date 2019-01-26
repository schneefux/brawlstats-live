import cv2
import logging

from pipe.pipe import Pipe
from state.enum.screen import Screen
from state.enum.brawler import Brawler
from matcher.template_matcher import TemplateMatcher

class VersusPipe(Pipe):
    """
    Extract information from the versus screen.
    """
    def __init__(self):
        self._matcher = TemplateMatcher()

    def start(self):
        self._matcher.load_templates("templates/brawler/*.png",
                                     1920, 1080)

    def process(self, frame, state):
        if state.screen not in [Screen.GEMGRAB_VERSUS] or \
                state.stream_config.screen_box is None:
            return {}

        matches = self._matcher.classify(frame,
                                         state.stream_config)
        if len(matches) == 0:
            # misclassified
            logging.warning(
                "Screen was classified as versus " +
                "but no brawler template matched")
            return {}

        ys = [match[1][1] for match in matches]
        average_y = sum(ys) / len(ys)
        blue_team = [Brawler(match[0]) for match in matches
                     if match[1][1] > average_y]
        red_team = [Brawler(match[0]) for match in matches
                     if match[1][1] < average_y]

        changes = {}

        if len(blue_team) == 3:
            changes["blue_team"] = blue_team
        if len(red_team) in [1, 3]: # 3v3 or 3v1 robots
            changes["red_team"] = red_team

        return changes
