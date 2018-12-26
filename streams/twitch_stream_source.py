import random

from api.video_buffer import VideoBuffer
from api.twitch import TwitchAPIClient
from streams.stream_source import StreamSource

class TwitchStreamSource(StreamSource):
    """
    Twitch buffered stream source.
    """
    def __init__(self, twitch_client_id, buffer_seconds):
        self._twitch = TwitchAPIClient(twitch_client_id)
        self._stream = VideoBuffer(buffer_seconds)

    def start(self, game_name, stream_resolution, fps,
              channel_name=None):
        game_id = self._twitch.get_game_id(game_name)

        if channel_name is None:
            channels = self._twitch.get_live_channel_names(game_id)
            random.shuffle(channels)
        else:
            channels = [channel_name]

        for channel in channels:
            stream = self._twitch.get_stream(channel,
                                             stream_resolution)
            if stream is not None:
                break
        else:
            return None

        self._stream.start(stream, fps)
        return channel

    def stop(self):
        self._stream.stop()

    @property
    def running(self):
        return self._stream.running

    def get_frame(self):
        return self._stream.read()
