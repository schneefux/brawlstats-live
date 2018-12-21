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

        logging.debug(
            "aspect ratio: %sknown, " +
            "current screen: %s, last screen: %s, " +
            "last match: %s, " +
            "fps: %2.2f, last frame: %2.2fs",

            "un" if state.stream_config.aspect_ratio_factor is None else "",
            state.current_screen,
            state.last_known_screen,
            state.last_match_result,
            len(self._durations) / sum(self._durations),
            duration
        )

        return {}
