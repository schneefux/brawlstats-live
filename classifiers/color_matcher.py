import cv2
import numpy as np
from enum import Enum

from classifiers.matcher import Matcher

class ColorMatcher(Matcher):
    def __init__(self, color_range):
        self._color_range = color_range

    def classify(self, frame, stream_config):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self._color_range.value[0],
                           self._color_range.value[1])
        changed_pixels = np.count_nonzero(mask)
        return changed_pixels / mask.size > self._color_range.value[2]


class ColorRange(Enum):
    # hsv [lower, upper, min pixel %]
    DAMAGE = (
        # red
        np.array([169, 128, 128], dtype=np.uint8),
        np.array([189, 255, 255], dtype=np.uint8),
        0.3
    )