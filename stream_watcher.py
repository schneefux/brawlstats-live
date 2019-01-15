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
from pipe.damage_pipe import DamagePipe
from pipe.gembar_pipe import GembarPipe

from state.game_state import GameState

class StreamWatcher(object):
    """
    Open a stream, process frames and update the state for it.
    """
    def __init__(self):
        self._realtime_pipeline = SyncPipeline((
            DevicePipe(),
            ScreenPipe(),
            DamagePipe(),
            GembarPipe()))
        self._deferred_pipeline = AsyncPipeline((
            VersusPipe(),
            DebugSink()))

    def start(self, stream_config, block_operations, video_url=None):
        self._block_deferred_pipeline = block_operations
        self.state = GameState(stream_config=stream_config)
        self._realtime_pipeline.start()
        self._deferred_pipeline.start()

        if video_url is None:
            streams = streamlink.streams(stream_config.url)
            stream = streams.get(str(stream_config.resolution) + "p") \
                or streams.get("best")
            if stream is None:
                raise Exception("Stream is invalid", stream_config.url)
            video_url = stream.url

        self._buffer = VideoBuffer()
        self._buffer.start(video_url, stream_config.max_fps,
            stream_config.resolution, block_read=block_operations)

    def stop(self):
        self._deferred_pipeline.stop()
        self._buffer.stop()

    @property
    def running(self):
        return self._deferred_pipeline.running and self._buffer.running

    def process(self):
        frame = self._buffer.get()

        new_state = evolve(self.state,
            timestamp=time.time(),
            seconds=self._buffer.seconds)

        # process sync tasks
        changes = self._realtime_pipeline.process(frame, new_state)
        new_state = evolve(new_state, **changes)

        # push tasks to async pipeline
        self._deferred_pipeline.process(frame, new_state)

        # block if not watching a live stream
        while self._block_deferred_pipeline and self._deferred_pipeline.processing:
            pass

        # get changes from this frame (if blocking) or previous frame
        changes = self._deferred_pipeline.reset_changes()
        new_state = evolve(new_state, **changes)

        self.state = new_state
        return frame.copy(), self.state
