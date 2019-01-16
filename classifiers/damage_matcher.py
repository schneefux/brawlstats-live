import cv2
import numpy as np

from classifiers.matcher import Matcher

class DamageMatcher(Matcher):
    damage_range = (
        np.array([135, 120, 110], dtype=np.uint8),
        np.array([180, 180, 180], dtype=np.uint8)
    )
    damage_match_threshold = 0.1

    def classify(self, frame, stream_config):
        screen_box = stream_config.screen_box
        frame = frame[screen_box[0][1]:screen_box[1][1],
                      screen_box[0][0]:screen_box[1][0]]

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.damage_range[0],
                           self.damage_range[1])
        matching_pixels = np.count_nonzero(mask)
        match_ratio = matching_pixels / mask.size
        return match_ratio > self.damage_match_threshold