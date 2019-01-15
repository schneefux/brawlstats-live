import cv2
import numpy as np

from classifiers.matcher import Matcher

class BlueGembarMatcher(Matcher):
    # hsv: h between 0 and 180
    blue_active_range = (
        np.array([90, 215, 210], dtype=np.uint8),
        np.array([115, 255, 255], dtype=np.uint8),
    )
    blue_inactive_range = (
        np.array([90, 215, 130], dtype=np.uint8),
        np.array([115, 255, 165], dtype=np.uint8),
    )
    blue_highlight_range = (
        np.array([80, 130, 230], dtype=np.uint8),
        np.array([120, 170, 255], dtype=np.uint8),
    )

    def classify(self, frame, stream_config):
        screen_box = stream_config.screen_box
        frame = frame[screen_box[0][1]:screen_box[1][1],
                      screen_box[0][0]:screen_box[1][0]]

        y0 = int(frame.shape[0] * 0.03)
        y1 = int(frame.shape[0] * 0.07)
        frame = frame[y0:y1, :int(frame.shape[1]/3)]

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        active_mask = cv2.inRange(hsv, self.blue_active_range[0],
                                  self.blue_active_range[1])
        inactive_mask = cv2.inRange(hsv, self.blue_inactive_range[0],
                                    self.blue_inactive_range[1])
        highlight_mask = cv2.inRange(hsv, self.blue_highlight_range[0],
                                     self.blue_highlight_range[1])
        active_pixels = np.count_nonzero(active_mask) + np.count_nonzero(highlight_mask)
        inactive_pixels = np.count_nonzero(inactive_mask)
        total_pixels = active_pixels + inactive_pixels
        return active_pixels / total_pixels if total_pixels > 0 else 0
        
        
class RedGembarMatcher(Matcher):
    red_active_range = (
        np.array([150, 200, 140], dtype=np.uint8),
        np.array([180, 255, 240], dtype=np.uint8),
    )
    red_inactive_range = (
        np.array([160, 220, 10], dtype=np.uint8),
        np.array([180, 255, 100], dtype=np.uint8),
    )

    def classify(self, frame, stream_config):
        screen_box = stream_config.screen_box
        frame = frame[screen_box[0][1]:screen_box[1][1],
                      screen_box[0][0]:screen_box[1][0]]

        y0 = int(frame.shape[0] * 0.03)
        y1 = int(frame.shape[0] * 0.07)
        frame = frame[y0:y1, int(frame.shape[1]*2/3):]
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        active_mask = cv2.inRange(hsv, self.red_active_range[0],
                                  self.red_active_range[1])
        inactive_mask = cv2.inRange(hsv, self.red_inactive_range[0],
                                    self.red_inactive_range[1])
        active_pixels = np.count_nonzero(active_mask)
        inactive_pixels = np.count_nonzero(inactive_mask)
        total_pixels = active_pixels + inactive_pixels
        return active_pixels / total_pixels if total_pixels > 0 else 0