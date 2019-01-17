import cv2
import numpy as np

from matcher.matcher import Matcher

class GembarMatcher(Matcher):
    # hsv values with h between 0 and 180
    active_range = None
    inactive_range = None
    highlight_range = None
    is_left = None

    def classify(self, frame, stream_config):
        screen_box = stream_config.screen_box
        frame = frame[screen_box[0][1]:screen_box[1][1],
                      screen_box[0][0]:screen_box[1][0]]

        y0 = int(frame.shape[0] * 0.03)
        y1 = int(frame.shape[0] * 0.07)

        if self.is_left:
            frame = frame[y0:y1, :int(frame.shape[1]/4)]
        else:
            frame = frame[y0:y1, int(frame.shape[1]/4*3):]

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        inactive_mask = cv2.inRange(hsv, self.inactive_range[0],
                                    self.inactive_range[1])
        inactive_pixels = np.count_nonzero(inactive_mask)

        active_mask = cv2.inRange(hsv, self.active_range[0],
                                  self.active_range[1])
        active_pixels = np.count_nonzero(active_mask)

        if self.highlight_range is not None:
            highlight_mask = cv2.inRange(hsv, self.highlight_range[0],
                                        self.highlight_range[1])
            active_pixels += np.count_nonzero(highlight_mask)

        total_pixels = active_pixels + inactive_pixels
        return active_pixels / total_pixels if total_pixels > 0 else 0


class BlueGembarMatcher(GembarMatcher):
    # hsv: h between 0 and 180
    active_range = (
        np.array([90, 215, 210], dtype=np.uint8),
        np.array([115, 255, 255], dtype=np.uint8),
    )
    inactive_range = (
        np.array([90, 215, 130], dtype=np.uint8),
        np.array([115, 255, 165], dtype=np.uint8),
    )
    highlight_range = (
        np.array([80, 130, 230], dtype=np.uint8),
        np.array([120, 170, 255], dtype=np.uint8),
    )
    is_left = True
        
        
class RedGembarMatcher(GembarMatcher):
    active_range = (
        np.array([150, 200, 140], dtype=np.uint8),
        np.array([180, 255, 240], dtype=np.uint8),
    )
    inactive_range = (
        np.array([160, 220, 30], dtype=np.uint8),
        np.array([180, 255, 100], dtype=np.uint8),
    )
    is_left = False