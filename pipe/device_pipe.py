import cv2
import numpy as np
from attr import evolve

from pipe.pipe import Pipe
from state.enum.screen import Screen

class DevicePipe(Pipe):
    """
    Detect the embedded game screen inside the frame.
    """
    def start(self):
        self._movement_map = None
        self._last_frame = None
        self._decay = 0.2

    def process(self, frame, state):
        if self._decay <= 0.05:
            return {}

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if self._last_frame is None:
            self._movement_map = np.zeros(gray_frame.shape,
                                          np.float)
            self._last_frame = gray_frame
            return {}

        diff = cv2.absdiff(gray_frame, self._last_frame)
        # ignore noise from compression artifacts
        diff = cv2.threshold(diff, 8, 255, cv2.THRESH_BINARY)[1]

        total_pixels   = diff.shape[0] * diff.shape[1]
        changed_pixels = np.count_nonzero(diff)
        changed_ratio  = float(changed_pixels) / total_pixels

        # assuming that the game's screen takes up at least 1/3
        if changed_ratio < 0.33:
            return {}

        cv2.accumulateWeighted(diff,
                self._movement_map,
                changed_ratio * self._decay)

        if self._movement_map.max() == 0:
            return {}

        # convert frame of floats to 1 channel gray
        movement_frame = cv2.convertScaleAbs(
            self._movement_map,
            alpha=255.0/self._movement_map.max())

        # smoothen for better contour performance
        movement_frame = cv2.blur(
            movement_frame, (int(gray_frame.shape[0]/10),
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
            return {}

        # find largest area
        x1, y1, w, h = sorted(rects,
                      key=lambda rect: rect[2]*rect[3],
                      reverse=True)[0]

        if h > w:
            # all devices are assumed to be landscape
            return {}

        self._last_frame = gray_frame

        stream_config = evolve(state.stream_config,
                               screen_box=((x1, y1),
                                           (x1+w, y1+h)))

        # slowly freeze the screen box after a good full screen transition
        if state.screen == Screen.LOADING:
            self._decay /= 2.0

        return {
            "stream_config": stream_config
        }
