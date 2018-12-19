import numpy
import random
import requests
import streamlink
import subprocess
from threading import Thread
from queue import Queue

class StreamSource(object):
    def get_frame(self):
        pass


class TwitchStream(StreamSource):
    def __init__(self, stream_resolution, twitch_client_id):
        # TODO close streams
        self._twitch_headers = { "Client-ID": twitch_client_id }
        self.channel, stream = self._get_random_channel(
            stream_resolution)
        self._stream = VideoStreamer(
            stream, 128, "{}p".format(stream_resolution), 10)

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
        return self._stream.wait_and_read()


# based on https://github.com/DanielTea/rage-analytics/blob/8e20121794478bda043df4d903aa8709f3ac79fc/engine/realtime_VideoStreamer.py
class VideoStreamer:
    '''
    Buffer a stream using ffmpeg, yielding every nth frame.
    '''
    def __init__(self, stream, buffer_size=128, resolution="720p", n_frame=10):
        self._n_frame = n_frame

        # initialize the queue used to store frames read from
        # the video stream
        self._Q = Queue(maxsize=buffer_size)
        if self._create_pipe(stream, resolution):
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
            'ffmpeg', "-i", stream.url,
                      "-loglevel", "quiet",  # no text output
                      "-an",  # disable audio
                      "-f", "image2pipe",
                      "-pix_fmt", "bgr24",
                      "-vcodec", "rawvideo", "-"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        return True

    def _start_buffer(self):
        # start a thread to read frames from the file video stream
        t = Thread(target=self._update_buffer_forever, args=())
        t.daemon = True
        t.start()

    def _update_buffer_forever(self):
        frames = 0

        while True:
            if frames % self._n_frame == 0:
                raw_image = self._pipe.stdout.read(
                    self._byte_length * self._byte_width * 3)

                frame = numpy.fromstring(raw_image, dtype='uint8')\
                    .reshape((self._byte_width, self._byte_length, 3))

                if not self._Q.full():
                    self._Q.put(frame)

            frames += 1

    def wait_and_read(self):
        while self._Q.qsize() == 0:
            pass
        return self._Q.get()
