import os
import cv2
import random
import requests
import streamlink
from classifier import Classifier

class StreamSource(object):
    def get_frame(self):
        pass


class TwitchStream(StreamSource):
    def __init__(self, stream_resolution, twitch_client_id):
        # TODO close streams later
        self._twitch_headers = { "Client-ID": twitch_client_id }
        self._resolution_p = "{}p".format(stream_resolution)

        self.channel, self._http_stream, buffer_file = self._get_stream()
        self._file_stream = open(buffer_file, "wb")
        self._flush()
        self._stream = cv2.VideoCapture(buffer_file)

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

    def _get_stream(self):
        channels = self._get_twitch_channel_names(self._get_game_id())
        random.shuffle(channels)
        for channel in channels:
            # get Twitch stream
            streams = streamlink.streams(
                "https://www.twitch.tv/" + channel)
            if self._resolution_p in streams:
                break

        buffer_file = "/tmp/" + channel + ".mpg"
        stream = streams[self._resolution_p].open()
        return channel, stream, buffer_file

    def _flush(self):
        '''
        Write data from http buffer to file buffer.
        '''
        self._file_stream.write(self._http_stream.read(-1))

    def get_frame(self):
        '''
        Skip all frames from the stream and return the last.
        '''
        # TODO this is quite an ugly workaround
        # might want to try this instead https://github.com/DanielTea/rage-analytics/blob/8e20121794478bda043df4d903aa8709f3ac79fc/engine/realtime_VideoStreamer.py
        last_frame = None
        self._flush()
        while True:
            # empty file buffer until no data
            _, frame = self._stream.read()
            if frame is None:
                # TODO suppress errors on console
                break
            last_frame = frame
        return last_frame
