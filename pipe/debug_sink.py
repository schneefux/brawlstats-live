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
            "current screen: %s, last screen: %s, " +
            "last match: %s, blue: %s, red: %s, " +
            "fps: %2.2f, last frame: %2.2fs",

            state.current_screen,
            state.last_known_screen,
            state.last_match_result,
            ",".join([b.name for b in state.blue_team]),
            ",".join([b.name for b in state.red_team]),
            len(self._durations) / sum(self._durations),
            duration
        )

        return {}
