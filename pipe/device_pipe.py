import cv2
import numpy as np
from attr import evolve

from pipe.pipe import Pipe
from state.enum.screen import Screen

class DevicePipe(Pipe):
    """
    Detect the embedded game screen inside the frame.
    """
    def process(self, frame, state):
        stream_config = state.stream_config
        # TODO move the below code into a classifier/

        if stream_config.screen_box_sensitivity == 0.0:
            # full screen mode was requested
            return {
                "stream_config": evolve(stream_config,
                    # skip this branch time
                    screen_box_sensitivity=0.01,
                    screen_box=((0, 0), frame.shape[:2][::-1]))
            }

        if stream_config.screen_box_sensitivity <= 0.05:
            return {}

        if stream_config.previous_frame is None:
            # initialize
            return {
                "stream_config": evolve(stream_config,
                    movement_frame=np.zeros(frame.shape[:2], np.float),
                    previous_frame=frame)
            }

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_last_frame = cv2.cvtColor(stream_config.previous_frame,
            cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(gray_frame, gray_last_frame)
        # ignore noise from compression artifacts
        diff = cv2.threshold(diff, 8, 255, cv2.THRESH_BINARY)[1]

        changed_ratio = np.count_nonzero(diff) / diff.size
        # assuming that the game's screen takes up at least 1/3
        if changed_ratio < 0.33:
            return {}

        movement_frame = stream_config.movement_frame
        cv2.accumulateWeighted(diff,
            movement_frame,
            changed_ratio * stream_config.screen_box_sensitivity)

        if movement_frame.max() == 0:
            return {}
        
        stream_config = evolve(stream_config,
            movement_frame=movement_frame)

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
            return {}

        # find largest area
        x1, y1, w, h = sorted(rects,
                      key=lambda rect: rect[2]*rect[3],
                      reverse=True)[0]

        if h > w:
            # all devices are assumed to be landscape
            return {}

        stream_config = evolve(stream_config,
            previous_frame=frame,
            screen_box=((x1, y1),
                        (x1+w, y1+h)))

        # slowly freeze the screen box after a good full screen transition
        if state.screen == Screen.LOADING:
            stream_config = evolve(stream_config,
                screen_box_sensitivity=stream_config.screen_box_sensitivity / 2.0)

        return {
            "stream_config": stream_config
        }
