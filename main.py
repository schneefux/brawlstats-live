#!/usr/bin/env python3
import cv2
import sys
import time
import config
import random
import logging
import coloredlogs
from threading import Thread
from flask import Flask, jsonify

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

if len(sys.argv) > 2 and sys.argv[2] in ["-s", "--server"]:
    app = Flask(__name__)

    @app.route("/state")
    def get_state(channel):
        return jsonify({
            "screen": watcher.state.screen.name \
                if watcher.state.screen is not None else None,
            "last_match_result": watcher.state.last_match_result.name \
                if watcher.state.last_match_result is not None else None,
            "blue_team": [b.name for b in watcher.state.blue_team] \
                if watcher.state.blue_team is not None else [],
            "red_team": [b.name for b in watcher.state.red_team] \
                if watcher.state.red_team is not None else []
        })

    thread = Thread(target=app.run)
    thread.daemon = True
    thread.start()

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