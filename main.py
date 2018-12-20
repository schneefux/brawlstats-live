#!/usr/bin/env python3
# based on https://gist.github.com/kscottz/242176c5bdb282b0a327
# using streamlink instead of livestreamer https://streamlink.github.io/api_guide.html

import cv2
import time
import config
from stream import TwitchStream
from stream_watcher import StreamWatcher

stream = TwitchStream(
    config.stream_resolution, config.client_id)
watcher = StreamWatcher()
watcher.start(stream, config.max_fps, config)

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
cv2.destroyAllWindows()
