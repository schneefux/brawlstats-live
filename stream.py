import json
import random
import subprocess
import numpy as np
from threading import Thread
from twitch import TwitchAPIClient

class StreamSource(object):
    def get_frame(self):
        pass


class TwitchStream(StreamSource):
    def __init__(self, twitch_client_id):
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

        self._stream = VideoStreamer()
        self._stream.start(stream)

    def stop(self):
        self._stream.stop()

    def get_frame(self):
        return self._stream.read()


# based on https://github.com/DanielTea/rage-analytics/blob/8e20121794478bda043df4d903aa8709f3ac79fc/engine/realtime_VideoStreamer.py
class VideoStreamer(object):
    '''
    Buffer a stream using ffmpeg, yielding every nth frame.
    '''
    def start(self, stream):
        self._frame = None
        self._running = True
        self._create_pipe(stream)
        self._thread = Thread(
            target=self._update_buffer_forever, args=())
        self._thread.daemon = True
        self._thread.start()

    def _create_pipe(self, stream):
        probe_pipe = subprocess.Popen([
            "ffprobe", stream.url,
                       "-v", "error",
                       "-show_entries", "stream=width,height",
                       "-of", "json"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE)
        video_info = probe_pipe.stdout.read().decode("utf8")
        video_info = json.loads(video_info)["streams"]
        video_info = next(
            data for data in video_info
            if len(data.keys()) > 0
        )
        probe_pipe.terminate()

        self._byte_length = video_info["width"]
        self._byte_width  = video_info["height"]

        self._pipe = subprocess.Popen([
            "ffmpeg", "-i", stream.url,
                      "-loglevel", "quiet", # no text output
                      "-an", # disable audio
                      "-f", "image2pipe",
                      "-pix_fmt", "bgr24",
                      "-vcodec", "rawvideo", "-"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE)

        self._frame = self._read_frame()

    def stop(self):
        self._pipe.terminate()
        self._running = False

    def _read_frame(self):
        raw_image = self._pipe.stdout.read(
            self._byte_length * self._byte_width * 3)
        return np.fromstring(raw_image, dtype="uint8")\
            .reshape((self._byte_width, self._byte_length, 3))

    def _update_buffer_forever(self):
        while self._running:
            self._frame = self._read_frame()

    def read(self):
        return self._frame
