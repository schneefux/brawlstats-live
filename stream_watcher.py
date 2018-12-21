import cv2
import time
from attr import evolve
from threading import Timer

from pipe.pipe import Pipe
from pipe.sync_pipeline import SyncPipeline
from pipe.async_pipeline import AsyncPipeline
from pipe.debug_sink import DebugSink
from pipe.screen_pipe import ScreenPipe
from pipe.loading_versus_pipe import LoadingVersusPipe
from pipe.victory_defeat_pipe import VictoryDefeatPipe

from state.game_state import GameState

class StreamWatcher(object):
    def __init__(self):
        self._realtime_pipeline = SyncPipeline((
            ScreenPipe(), ))
        self._deferred_pipeline = AsyncPipeline((
            LoadingVersusPipe(),
            VictoryDefeatPipe(),
            DebugSink()))

    def start(self, stream, config, stream_config):
        self.state = GameState(stream_config=stream_config)
        self._stream = stream
        self._fps = config.max_fps
        self._running = True
        self._realtime_pipeline.start()
        self._deferred_pipeline.start()
        self._tick()

    def stop(self):
        self._running = False
        self._timer.cancel()

    def _tick(self):
        if not self._running:
            return

        start_time = time.time()
        frame = self._stream.get_frame()

        # get any changes from previous tick
        changes = self._deferred_pipeline.get_change()
        new_state = evolve(self.state,
                           timestamp=start_time,
                           **changes)
        changes = self._realtime_pipeline.process(frame, new_state)
        new_state = evolve(new_state, **changes)
        # push tasks to thread
        self._deferred_pipeline.process(frame, new_state)

        self.state = new_state

        seconds_until_next = max(
            1.0/self._fps - (time.time() - start_time), 0)

        self._timer = Timer(seconds_until_next, self._tick)
        self._timer.daemon = True
        self._timer.start()
