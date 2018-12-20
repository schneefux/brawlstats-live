import json
import random
import requests
import streamlink
import subprocess
import numpy as np
from threading import Thread

class StreamSource(object):
    def get_frame(self):
        pass


class TwitchStream(StreamSource):
    def __init__(self, stream_resolution, twitch_client_id):
        # TODO close streams
        self.stream_resolution = stream_resolution
        self._twitch_headers = { "Client-ID": twitch_client_id }
        self.channel, stream = self._get_random_channel(
            stream_resolution)
        self._stream = VideoStreamer(stream)

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
    def __init__(self, stream):
        self._frame = None
        self._create_pipe(stream)
        self._start_buffer()

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

    def _start_buffer(self):
        t = Thread(target=self._update_buffer_forever, args=())
        t.daemon = True
        t.start()

    def _read_frame(self):
        raw_image = self._pipe.stdout.read(
            self._byte_length * self._byte_width * 3)
        return np.fromstring(raw_image, dtype="uint8")\
            .reshape((self._byte_width, self._byte_length, 3))

    def _update_buffer_forever(self):
        while True:
            self._frame = self._read_frame()

    def read(self):
        return self._frame
