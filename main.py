#!/usr/bin/env python3

import cv2
import sys
import time
import config
import logging
import numpy as np

from state.stream_config import StreamConfig
from streams.twitch_stream_source import TwitchStreamSource
from stream_watcher import StreamWatcher

logging.basicConfig(level=logging.DEBUG)

stream = TwitchStreamSource(config.client_id, config.buffer_seconds)
channel = sys.argv[1] if len(sys.argv) > 1 else None
channel = stream.start("Brawl Stars",
                       config.stream_resolution,
                       config.max_ui_fps,
                       channel)

stream_config = StreamConfig(resolution=config.stream_resolution,
                             channel=channel)

watcher = StreamWatcher()
watcher.start(stream, config, stream_config)

logging.info("Watching %s's channel", channel)

while watcher.running:
    frame = stream.get_frame()

    box = watcher.state.stream_config.screen_box
    if box is not None:
        cv2.rectangle(frame, box[0], box[1],
                      (255, 0, 0), 2)
    cv2.imshow("frame", frame)

    key = 0xFF & cv2.waitKey(int(1.0/config.max_ui_fps*1000))
    if key == 27:
        # ESC: quit
        break
    if key == 32:
        # space: screenshot
        filename = "{}_{}.png".format(channel, int(time.time()))
        cv2.imwrite(filename,
                    frame[box[0][1]:box[1][1], box[0][0]:box[1][0]])

watcher.stop()
stream.stop()
cv2.destroyAllWindows()
