#!/usr/bin/env python3
import cv2
import sys
import time
import config
import random
import logging

from api.twitch import TwitchAPIClient
from api.video_buffer import VideoBuffer
from stream_watcher import StreamWatcher
from state.stream_config import StreamConfig

logging.basicConfig(level=logging.DEBUG)

twitch = TwitchAPIClient(config.client_id)

brawl_star_id = twitch.get_game_id("Brawl Stars")
channels = twitch.get_live_channel_names(brawl_star_id)
channel = sys.argv[1] if len(sys.argv) > 1 \
    else random.choice(channels)

stream = twitch.get_stream(channel, config.stream_resolution)
buffer = VideoBuffer(config.buffer_seconds)
buffer.start(stream, config.max_ui_fps, config.stream_resolution)

stream_config = StreamConfig(resolution=config.stream_resolution,
                             channel=channel)

watcher = StreamWatcher()
watcher.start(buffer, config.max_fps, stream_config)

logging.info("Watching %s's channel", channel)

while watcher.running:
    frame = buffer.read()

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
cv2.destroyAllWindows()
