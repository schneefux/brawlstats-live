import numpy as np
import random
import requests
import streamlink
import subprocess
from threading import Thread

class StreamSource(object):
    def get_frame(self):
        pass


class TwitchStream(StreamSource):
    def __init__(self, stream_resolution, twitch_client_id):
        # TODO close streams
        self._twitch_headers = { "Client-ID": twitch_client_id }
        self.channel, stream = self._get_random_channel(
            stream_resolution)
        self._stream = VideoStreamer(stream,
                                     "{}p".format(stream_resolution))

    def _get_game_id(self):
        #r = requests.get("https://api.twitch.tv/helix/games?name=Brawl+Stars",
        #                 headers=self._twitch_headers)
        #twitch_game_id = r.json()["data"][0]["id"]
        twitch_game_id = "497497" # Brawl Stars
        return twitch_game_id

    def _get_twitch_channel_names(self, game_id):
        r = requests.get("https://api.twitch.tv/helix/streams" +
                         "?first=10&language=en&game_id=" + game_id,
                         headers=self._twitch_headers)
        return [data["user_name"] for data in r.json()["data"]]

    def _get_random_channel(self, resolution):
        resolution_p = "{}p".format(resolution)
        channels = self._get_twitch_channel_names(self._get_game_id())
        random.shuffle(channels)
        for channel in channels:
            # get Twitch stream
            streams = streamlink.streams(
                "https://www.twitch.tv/" + channel)
            if resolution_p in streams:
                return channel, streams[resolution_p]

    def get_frame(self):
        return self._stream.read()


# based on https://github.com/DanielTea/rage-analytics/blob/8e20121794478bda043df4d903aa8709f3ac79fc/engine/realtime_VideoStreamer.py
class VideoStreamer:
    '''
    Buffer a stream using ffmpeg, yielding every nth frame.
    '''
    def __init__(self, stream, resolution):
        self._frame = None
        self._create_pipe(stream, resolution)
        self._start_buffer()

    def _create_pipe(self, stream, resolution):
        resolutions = {
            "360p": [640, 360],
            "480p": [852, 480],
            "720p": [1280, 720],
            "1080p": [1920, 1080]
        }

        self._byte_length = resolutions[resolution][0]
        self._byte_width = resolutions[resolution][1]
        self._pipe = subprocess.Popen([
            "ffmpeg", "-i", stream.url,
                      "-loglevel", "quiet", # no text output
                      "-an", # disable audio
                      "-f", "image2pipe",
                      "-pix_fmt", "bgr24",
                      "-vcodec", "rawvideo", "-"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE)

    def _start_buffer(self):
        t = Thread(target=self._update_buffer_forever, args=())
        t.daemon = True
        t.start()

    def _update_buffer_forever(self):
        while True:
            raw_image = self._pipe.stdout.read(
                self._byte_length * self._byte_width * 3)
            self._frame = np.fromstring(raw_image, dtype="uint8")\
                .reshape((self._byte_width, self._byte_length, 3))

    def read(self):
        while self._frame is None:
            pass
        return self._frame
