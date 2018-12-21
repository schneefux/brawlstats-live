#!/usr/bin/env python3

import cv2
import time
import config
from state.stream_config import StreamConfig
from stream import TwitchStream
from stream_watcher import StreamWatcher

stream_config = StreamConfig(resolution=config.stream_resolution,
                             aspect_ratio_factor=None)

stream = TwitchStream(config.client_id)
stream.start("Brawl Stars", stream_config.resolution)

watcher = StreamWatcher()
watcher.start(stream, config, stream_config)

while True:
    frame = stream.get_frame()
    cv2.imshow("frame", frame)

    key = 0xFF & cv2.waitKey(int(1.0/config.max_ui_fps*1000))
    if key == 27:
        # ESC: quit
        break
    if key == 32:
        # space: screenshot
        filename = "{}_{}.png".format(stream.channel, int(time.time()))
        cv2.imwrite(filename, frame)

watcher.stop()
stream.stop()
cv2.destroyAllWindows()
