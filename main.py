#!/usr/bin/env python3
# based on https://gist.github.com/kscottz/242176c5bdb282b0a327
# using streamlink instead of livestreamer https://streamlink.github.io/api_guide.html

import cv2
import time
import config
from classifier import Classifier
from stream import TwitchStream

stream = TwitchStream(
    config.stream_resolution, config.client_id)
classifier = Classifier(config.stream_resolution)
classifier.load_templates(
    "templates/*.png", config.template_resolution)

while True:
    frame = stream.get_frame()
    cv2.imshow("frame", frame)

    matching_template_name = classifier.classify_image(frame)
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

cv2.destroyAllWindows()
