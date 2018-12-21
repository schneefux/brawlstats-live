import random

from lib.video_buffer import VideoBuffer
from lib.twitch import TwitchAPIClient
from streams.stream_source import StreamSource

class TwitchStreamSource(StreamSource):
    """
    Twitch buffered stream source.
    """
    def __init__(self, twitch_client_id):
        self.channel = None
        self._twitch = TwitchAPIClient(twitch_client_id)

    def start(self, game_name, stream_resolution):
        game_id = self._twitch.get_game_id(game_name)
        channels = self._twitch.get_live_channel_names(game_id)

        stream = None
        while stream is None:
            self.channel = random.choice(channels)
            # pick a stream with the correct resolution
            stream = self._twitch.get_stream(
                self.channel, stream_resolution)

        self._stream = VideoBuffer()
        self._stream.start(stream)

    def stop(self):
        self._stream.stop()

    def get_frame(self):
        return self._stream.read()

