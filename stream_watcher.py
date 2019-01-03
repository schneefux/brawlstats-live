import time
import streamlink
from attr import evolve

from api.video_buffer import VideoBuffer
from pipe.pipe import Pipe
from pipe.sync_pipeline import SyncPipeline
from pipe.async_pipeline import AsyncPipeline
from pipe.debug_sink import DebugSink
from pipe.screen_pipe import ScreenPipe
from pipe.versus_pipe import VersusPipe
from pipe.device_pipe import DevicePipe
from pipe.victory_defeat_pipe import VictoryDefeatPipe

from state.game_state import GameState

class StreamWatcher(object):
    """
    Open a stream, process frames and update the state for it.
    """
    def __init__(self):
        self._realtime_pipeline = SyncPipeline((
            DevicePipe(),
            ScreenPipe()))
        self._deferred_pipeline = AsyncPipeline((
            VersusPipe(),
            VictoryDefeatPipe(),
            DebugSink()))

    def start(self, stream_config, fps, realtime):
        self.state = GameState(stream_config=stream_config)
        self._realtime_pipeline.start()
        self._deferred_pipeline.start()

        streams = streamlink.streams(stream_config.url)
        stream = streams.get(str(stream_config.resolution) + "p") \
            or streams.get("best")
        if stream is None:
            raise Exception("Stream is invalid", stream_config.url)

        self._buffer = VideoBuffer()
        self._buffer.start(
            stream, fps, stream_config.resolution, True)

    def stop(self):
        self._deferred_pipeline.stop()
        self._buffer.stop()

    @property
    def running(self):
        return self._deferred_pipeline.running and self._buffer.running

    def process(self):
        frame = self._buffer.get()

        new_state = evolve(self.state, timestamp=time.time())
        # get any changes from previous frame
        changes = self._deferred_pipeline.get_change()
        new_state = evolve(new_state, **changes)
        changes = self._realtime_pipeline.process(frame, new_state)
        new_state = evolve(new_state, **changes)
        # push tasks to thread
        self._deferred_pipeline.process(frame, new_state)

        self.state = new_state
        return frame.copy(), self.state
