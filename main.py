#!/usr/bin/env python3
# based on https://gist.github.com/kscottz/242176c5bdb282b0a327
# using streamlink instead of livestreamer https://streamlink.github.io/api_guide.html

import os
import cv2
import time
import requests
import streamlink
from classifier import Classifier
import config

TWITCH_HEADERS = { "Client-ID": config.client_id }

stream_resolution_p = "{}p".format(config.stream_resolution)

#r = requests.get("https://api.twitch.tv/helix/games?name=Brawl+Stars",
#                 headers=TWITCH_HEADERS)
#twitch_game_id = r.json()["data"][0]["id"]
twitch_game_id = "497497" # Brawl Stars

r = requests.get("https://api.twitch.tv/helix/streams" +
                 "?first=10&language=en&game_id=" + twitch_game_id,
                 headers=TWITCH_HEADERS)
for channel_data in r.json()["data"]:
    channel = channel_data["user_name"]
    buffer_file = "/tmp/" + channel + ".mpg"

    # get Twitch stream
    streams = streamlink.streams("https://www.twitch.tv/" + channel)
    if stream_resolution_p not in streams:
        # try next
        continue

    print("watching {}'s stream".format(channel))
    # should be same as template resolution!
    stream = streams[stream_resolution_p].open()
    break

buffer = open(buffer_file, "wb")
print("buffering")
buffer.write(stream.read(-1))

def get_last_frame():
    '''
    Skip all frames from the stream and return the last.
    '''
    # TODO this is quite an ugly workaround
    # might want to try this instead https://github.com/DanielTea/rage-analytics/blob/8e20121794478bda043df4d903aa8709f3ac79fc/engine/realtime_VideoStreamer.py
    last_frame = None
    while True:
        # stream buffer -> file buffer
        buffer.write(stream.read(-1))
        while True:
            # empty file buffer until no data
            _, frame = cap.read()
            if frame is None:
                # TODO suppress errors on console
                break
            last_frame = frame
        if last_frame is not None:
            return last_frame
        print("buffering")


cap = cv2.VideoCapture(buffer_file)
classifier = Classifier(config.stream_resolution)
classifier.load_templates("templates/*.png",
                          config.template_resolution)

while True:
    frame = get_last_frame()
    cv2.imshow("frame", frame)

    matching_template_name = classifier.classify_image(frame, channel)
    if matching_template_name is not None:
        print("current frame shows {}!"
              .format(matching_template_name))

    # release and check for ESC
    key = 0xFF & cv2.waitKey(1)
    if key == 27:
        # ESC: quit
        break
    if key == 32:
        # space: screenshot
        filename = channel + "_" + str(int(time.time())) + ".png"
        cv2.imwrite(filename, frame)

buffer.close()
stream.close()
cv2.destroyAllWindows()
os.remove(buffer_file)
