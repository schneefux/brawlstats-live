#!/usr/bin/env python3
# based on https://gist.github.com/kscottz/242176c5bdb282b0a327
# using streamlink instead of livestreamer https://streamlink.github.io/api_guide.html

import os
import io
import cv2
import time
import glob
import streamlink
import numpy as np

CHANNEL = "ohryantv"
BUFFER = "/tmp/" + CHANNEL + ".mpg"

# get Twitch stream
streams = streamlink.streams("https://www.twitch.tv/" + CHANNEL)

# buffer first frame to file
print("Buffering")
stream = streams["480p"].open() # ['audio_only', '160p', '360p', '480p', '720p', 'worst', 'best']
buffer = open(BUFFER, "wb")
buffer.write(stream.read(854*480*3))

# open templates and stream
cap = cv2.VideoCapture(BUFFER)
templates = dict()
for fp in glob.glob("templates/*.png"):
    template = cv2.imread(fp)
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    name = os.path.basename(os.path.splitext(fp)[0])
    templates[name] = template
print("loaded templates {}".format(templates.keys()))

while True:
    for _ in range(10):
        ret, frame = cap.read()

    # https://www.docs.opencv.org/trunk/d4/dc6/tutorial_py_template_matching.html
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    threshold = 0.9
    # assumes that the dimension of the template source image and the comparison image are equal!
    for template_name, template in templates.items():
        match = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
        location = np.where(match >= threshold)
        for pt in zip(*location[::-1]):
            print("found a match for template {}".format(template_name))
            template_w, template_h = template.shape[::-1]
            cv2.rectangle(frame, pt, (pt[0] + template_w, pt[1] + template_h), (0, 0, 255), 2)

    cv2.imshow("frame", frame)

    # release and check for ESC
    if (0xFF & cv2.waitKey(1) == 27) or frame.size == 0:
        # write possible template file
        filename = CHANNEL + "_" + str(int(time.time())) + ".png"
        cv2.imwrite(filename, frame)
        break

    buffer.write(stream.read(-1))

buffer.close()
stream.close()
cv2.destroyAllWindows()
