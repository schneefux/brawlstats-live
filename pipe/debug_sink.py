import os
import cv2
import time
import logging

from pipe.sink import Sink

class DebugSink(Sink):
    """
    Log.
    """
    def start(self):
        self._durations = []

    def process(self, frame, state):
        duration = time.time() - state.timestamp
        self._durations.append(duration)
        if len(self._durations) > 10:
            self._durations = self._durations[1:]

        if state.stream_config.screen_box is not None and \
                state.screen is None:
            screen_box = state.stream_config.screen_box
            cut_frame = frame[screen_box[0][1]:screen_box[1][1],
                              screen_box[0][0]:screen_box[1][0]]
            path = "model/screen/dataset/new"
            if not os.path.exists(path):
                os.makedirs(path)
            cv2.imwrite("{}/{}.jpg".format(
                path, int(state.timestamp)), cut_frame)

        if sum(self._durations) == 0:
            fps = -1.0
        else:
            fps = len(self._durations) / sum(self._durations)

        logging.debug(
            "screen: %s (last result: %s), " +
            "%s vs. %s, " +
            "%2.2f max fps",
            state.screen or "unknown",
            state.last_match_result or "unknown",
            ",".join([b.name for b in state.blue_team]) or "unknown",
            ",".join([b.name for b in state.red_team]) or "unknown",
            fps
        )

        return {}
