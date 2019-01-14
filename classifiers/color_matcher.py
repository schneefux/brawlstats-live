import cv2
import numpy as np
from enum import Enum
from attr import attrs, attrib

from classifiers.matcher import Matcher

class ColorMatcher(Matcher):
    def __init__(self, color_range):
        self._color_range = color_range

    def classify(self, frame, stream_config):
        x0 = int(self._color_range.box[0][0] * frame.shape[1])
        x1 = int(self._color_range.box[1][0] * frame.shape[1])
        y0 = int(self._color_range.box[0][1] * frame.shape[0])
        y1 = int(self._color_range.box[1][1] * frame.shape[0])
        
        frame = frame[y0:y1, x0:x1]
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self._color_range.lower_color,
                           self._color_range.upper_color)
        matching_pixels = np.count_nonzero(mask)
        match_ratio = matching_pixels / mask.size
        return (match_ratio > self._color_range.threshold,
                match_ratio)


@attrs(frozen=True)
class ColorRange(object):
    # hsv
    lower_color = attrib()
    upper_color = attrib()
    threshold = attrib()
    # x1, y1, x2, y2
    box = attrib()

    @staticmethod
    def DAMAGE():
        return ColorRange(
            np.array([169, 128, 128], dtype=np.uint8),
            np.array([189, 255, 255], dtype=np.uint8),
            0.3,
            ((0.0, 0.0), (1.0, 1.0)))

    @staticmethod
    def GEMBAR_BLUE():
        return ColorRange(
            np.array([80, 110, 230], dtype=np.uint8),
            np.array([100, 255, 255], dtype=np.uint8),
            0.3,
            ((55/852.0, 20/420.0), (210/852.0, 25/420.0)))

    @staticmethod
    def GEMBAR_RED():
        return ColorRange(
            np.array([170, 200, 180], dtype=np.uint8),
            np.array([180, 255, 255], dtype=np.uint8),
            0.3,
            ((641/852.0, 20/420.0), (797/852.0, 25/420.0)))
