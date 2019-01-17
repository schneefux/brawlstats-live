import cv2
import numpy as np
from attr import evolve

from pipe.pipe import Pipe
from state.enum.screen import Screen
from matcher.device_matcher import DeviceMatcher

class DevicePipe(Pipe):
    """
    Detect the embedded game screen inside the frame.
    """
    def __init__(self):
        self._matcher = DeviceMatcher()

    def process(self, frame, state):
        stream_config = state.stream_config

        if stream_config.screen_box_sensitivity == 0.0:
            # full screen mode was requested, skip
            return {
                "stream_config": evolve(stream_config,
                    # skip this branch time
                    screen_box_sensitivity=-1.0,
                    screen_box=((0, 0), frame.shape[:2][::-1]))
            }

        if stream_config.screen_box_sensitivity <= 0.05:
            # screen is frozen, skip
            return {}

        if stream_config.previous_frame is None:
            # initialize, skip
            return {
                "stream_config": evolve(stream_config,
                    movement_frame=np.zeros(frame.shape[:2], np.float),
                    previous_frame=frame)
            }

        stream_config = evolve(stream_config,
            **self._matcher.classify(frame, stream_config))

        # slowly freeze the screen box after a good full screen transition
        if state.screen == Screen.LOADING:
            stream_config = evolve(stream_config,
                screen_box_sensitivity=stream_config.screen_box_sensitivity / 2.0)

        return {
            "stream_config": stream_config
        }
