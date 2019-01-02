import os
import cv2
import time
import logging

from pipe.sink import Sink

class DebugSink(Sink):
    """
    Log.
    """
    realtime = True

    def start(self):
        self._durations = []

    def process(self, frame, state):
        duration = time.time() - state.timestamp
        self._durations.append(duration)
        if len(self._durations) > 10:
            self._durations = self._durations[1:]

        if state.current_screen is not None:
            screen_box = state.stream_config.screen_box
            cut_frame = frame[screen_box[0][1]:screen_box[1][1],
                              screen_box[0][0]:screen_box[1][0]]
            path = "dataset/{}/".format(
                    state.current_screen.name.lower())
            if not os.path.exists(path):
                os.makedirs(path)
            cv2.imwrite("{}/{}_{}.jpg".format(
                path,
                state.stream_config.channel,
                int(state.timestamp)), cut_frame)

        logging.debug(
            "screen: %s (last: %s, result: %s), " +
            "%s vs. %s, " +
            "%2.2f max fps",
            state.current_screen or "unknown",
            state.last_known_screen or "unknown",
            state.last_match_result or "unknown",
            ",".join([b.name for b in state.blue_team]) or "unknown",
            ",".join([b.name for b in state.red_team]) or "unknown",
            len(self._durations) / sum(self._durations)
        )

        return {}
