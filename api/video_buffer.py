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
    def __init__(self, buffer_seconds=10.0):
        self.buffer_seconds = buffer_seconds
        self.running = False

    def start(self, url, fps, resolution, block_read):
        """
        Start the ffmpeg process and block until the first frame.
        """
        self.running = True
        self._block_read = block_read
        self._fps = fps
        self._buffer = queue.Queue(self._fps * self.buffer_seconds)
        self.seconds = 0.0
        self._start_pipe(url, resolution)
        while self._buffer.empty():
            pass

    def _start_pipe(self, url, resolution):
        probe_pipe = subprocess.Popen([
            "ffprobe", url,
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
            logging.warning(
                "video has different resolution than requested, rescaling")
            # rescale preserving aspect ratio
            ratio = resolution / float(video_info["height"])
            self._byte_length = round(video_info["width"] * ratio)
            self._byte_width = resolution
        else:
            self._byte_length = video_info["width"]
            self._byte_width  = video_info["height"]

        self._pipe = subprocess.Popen([
            "ffmpeg", "-i", url,
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

    def stop(self):
        if self.running:
            self._pipe.terminate()
            self.running = False

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
                self._buffer.put(frame, block=self._block_read)
            except queue.Full:
                # skip current and drop oldest
                logging.debug("stream buffer is full, dropping frames")
                self._buffer.get()

    def get(self):
        frame = self._buffer.get()
        self.seconds += 1.0 / self._fps
        return frame
