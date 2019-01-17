import cv2
import numpy as np
from attr import evolve

from matcher.matcher import Matcher

class DeviceMatcher(Matcher):
    """
    Detect the embedded game screen inside the frame.
    """
    def classify(self, frame, stream_config):
        changes = {}

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_last_frame = cv2.cvtColor(stream_config.previous_frame,
            cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(gray_frame, gray_last_frame)
        # ignore noise from compression artifacts
        diff = cv2.threshold(diff, 8, 255, cv2.THRESH_BINARY)[1]

        changed_ratio = np.count_nonzero(diff) / diff.size
        # assuming that the game's screen takes up at least 1/3
        if changed_ratio < 0.33:
            return changes

        movement_frame = stream_config.movement_frame
        cv2.accumulateWeighted(diff,
            movement_frame,
            changed_ratio * stream_config.screen_box_sensitivity)

        if movement_frame.max() == 0:
            return changes
        
        changes = {
            **changes,
            "movement_frame": movement_frame
        }

        # convert frame of floats to 1 channel gray
        movement_frame = cv2.convertScaleAbs(
            movement_frame,
            alpha=255.0/movement_frame.max())

        # smoothen for better contour performance
        movement_frame = cv2.blur(movement_frame,
            (int(gray_frame.shape[0]/10),
             int(gray_frame.shape[1]/5)))

        movement_frame = cv2.threshold(
            movement_frame,
            0, 255,
            cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        contours = cv2.findContours(
            movement_frame,
            cv2.RETR_EXTERNAL, # only match parent contours
            cv2.CHAIN_APPROX_SIMPLE)[1]

        rects = [cv2.boundingRect(contour) for contour in contours]

        if len(rects) == 0:
            return changes

        # find largest area
        x1, y1, w, h = sorted(rects,
            key=lambda rect: rect[2]*rect[3],
            reverse=True)[0]

        if h > w:
            # all devices are assumed to be landscape
            return changes

        return {
            **changes,
            "previous_frame": frame,
            "screen_box": ((x1, y1), (x1+w, y1+h))
        }