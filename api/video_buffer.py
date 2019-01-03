import json
import time
import queue
import logging
import subprocess
import numpy as np
from threading import Timer, Thread

class VideoBuffer(object):
    """
    Buffer a stream using ffmpeg.
    """
    def __init__(self, buffer_seconds):
        self.buffer_seconds = buffer_seconds
        self.running = False

    def start(self, stream, fps, resolution):
        self.running = True
        self._fps = fps
        self._last_frame = None
        self._buffer = queue.Queue(self._fps * self.buffer_seconds)
        self._create_pipe(stream, resolution)

    def _create_pipe(self, stream, resolution):
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

        if resolution != video_info["height"]:
            # rescale preserving aspect ratio
            ratio = resolution / float(video_info["height"])
            self._byte_length = round(video_info["width"] * ratio)
            self._byte_width = resolution
        else:
            self._byte_length = video_info["width"]
            self._byte_width  = video_info["height"]

        self._pipe = subprocess.Popen([
            "ffmpeg", "-i", stream.url,
                      "-loglevel", "quiet", # no text output
                      "-an", # disable audio
                      "-vf", "scale=-1:" + str(resolution),
                      "-f", "image2pipe",
                      "-pix_fmt", "bgr24",
                      "-r", str(self._fps),
                      "-vcodec", "rawvideo", "-"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE)

        self._thread = Thread(target=self._read_forever)
        self._thread.daemon = True
        self._thread.start()
        while self._buffer.empty():
            pass
        self._update_last_frame()

    def stop(self):
        if self.running:
            self._pipe.terminate()
            self.running = False

    def _update_last_frame(self):
        if self.running:
            try:
                self._last_frame = self._buffer.get_nowait()
            except queue.Empty:
                logging.debug("stream buffer is empty, keeping frame")

            self._timer = Timer(1.0/self._fps,
                                self._update_last_frame)
            self._timer.daemon = True
            self._timer.start()

    def _read_forever(self):
        while self.running:
            raw_image = self._pipe.stdout.read(
                self._byte_length * self._byte_width * 3)
            if len(raw_image) == 0:
                self.running = False
                return

            frame = np.fromstring(raw_image, dtype="uint8")\
                .reshape((self._byte_width, self._byte_length, 3))
            try:
                self._buffer.put_nowait(frame)
            except queue.Full:
                logging.debug("stream buffer is full, dropping frame")

    def read(self):
        return self._last_frame
