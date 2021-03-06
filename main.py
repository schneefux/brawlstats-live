#!/usr/bin/env python3
import cv2
import time
import config
import random
import logging
import argparse
import coloredlogs
from attr import evolve

from api.twitch import TwitchAPIClient
from stream_watcher import StreamWatcher
from state.stream_config import StreamConfig

coloredlogs.install(level="DEBUG")

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", action="store_true")
parser.add_argument("-l", "--live", action="store_true")
parser.add_argument("-r", "--random", action="store_true")
parser.add_argument("-F", "--fullscreen", action="store_true")
parser.add_argument("-u", "--url")
args = parser.parse_args()

if args.live:
    logging.warning("processing live stream")

if args.url is None:
    twitch = TwitchAPIClient(config.client_id)
    args.url = "https://www.twitch.tv/" + random.choice(
        twitch.get_live_channel_names(
            twitch.get_game_id("Brawl Stars")))

stream_config = StreamConfig(
    resolution=480,
    max_fps=config.max_fps,
    url=args.url)

if args.fullscreen:
    stream_config = evolve(stream_config,
        screen_box_sensitivity=0.0)

watcher = StreamWatcher()
watcher.start(stream_config,
    block_operations=not args.live,
    video_url=args.url if args.file else None)

logging.info("Watching %s", args.url)

while watcher.running:
    frame, state = watcher.process()
    preview = frame.copy()

    box = state.stream_config.screen_box
    if box is not None:
        cv2.rectangle(preview, box[0], box[1],
                        (255, 0, 0), 2)
    cv2.imshow("preview", preview)

    s_until_next = 1.0/state.stream_config.max_fps - (time.time()-state.timestamp)
    wait_ms = 1 if not args.live else max(1, int(1000*s_until_next))
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