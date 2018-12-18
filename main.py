#!/usr/bin/env python3
# based on https://gist.github.com/kscottz/242176c5bdb282b0a327
# using streamlink instead of livestreamer https://streamlink.github.io/api_guide.html

import os
import cv2
import time
import streamlink
import classifier

CHANNEL = "runickk"
BUFFER = "/tmp/" + CHANNEL + ".mpg"

# get Twitch stream
streams = streamlink.streams("https://www.twitch.tv/" + CHANNEL)

# should be same as template resolution!
stream = streams["480p"].open()
# common options: audio_only, 160p, 360p, 480p, 720p, worst, best
buffer = open(BUFFER, "wb")
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


cap = cv2.VideoCapture(BUFFER)

while True:
    frame = get_last_frame()
    cv2.imshow("frame", frame)

    matching_template_name = classifier.classify_image(frame, CHANNEL)
    if matching_template_name is not None:
        print(matching_template_name)

    # release and check for ESC
    key = 0xFF & cv2.waitKey(5)
    if key == 27:
        # ESC: quit
        break
    if key == 32:
        # space: screenshot
        filename = CHANNEL + "_" + str(int(time.time())) + ".png"
        cv2.imwrite(filename, frame)

buffer.close()
stream.close()
cv2.destroyAllWindows()
os.remove(BUFFER)
