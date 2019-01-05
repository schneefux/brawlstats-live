#!/usr/bin/env python3
import cv2
import sys
import time
import config
import random
import logging
import coloredlogs

from api.twitch import TwitchAPIClient
from stream_watcher import StreamWatcher
from state.stream_config import StreamConfig

coloredlogs.install(level="DEBUG")

twitch = TwitchAPIClient(config.client_id)

if len(sys.argv) > 1:
    if sys.argv[1].startswith("http"):
        url = sys.argv[1]
        realtime = False
    else:
        url = "https://www.twitch.tv/" + sys.argv[1]
        realtime = True
else:
    url = "https://www.twitch.tv/" + random.choice(
        twitch.get_live_channel_names(
            twitch.get_game_id("Brawl Stars")))
    realtime = True

if realtime:
    logging.warning("processing live stream")

stream_config = StreamConfig(
    resolution=config.stream_resolution, url=url)

watcher = StreamWatcher()
watcher.start(stream_config, config.max_fps, realtime)

logging.info("Watching %s", url)

while watcher.running:
    frame, state = watcher.process()
    preview = frame.copy()

    box = state.stream_config.screen_box
    if box is not None:
        cv2.rectangle(preview, box[0], box[1],
                      (255, 0, 0), 2)
    cv2.imshow("preview", preview)

    s_until_next = 1.0/config.max_fps - (time.time()-state.timestamp)
    wait_ms = 1 if not realtime else max(1, int(1000*s_until_next))
    key = 0xFF & cv2.waitKey(wait_ms)
    if key == 27:
        # ESC: quit
        watcher.stop()
    if key == 32:
        # space: screenshot
        cv2.imwrite("{}.png".format(int(time.time())),
                    frame[box[0][1]:box[1][1], box[0][0]:box[1][0]])

watcher.stop()
cv2.destroyAllWindows()
