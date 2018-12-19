#!/usr/bin/env python3
# based on https://gist.github.com/kscottz/242176c5bdb282b0a327
# using streamlink instead of livestreamer https://streamlink.github.io/api_guide.html

import cv2
import time
import config
from classifier import Classifier
from stream import TwitchStream
from threading import Thread

class backgroundThread(Thread):
    def __init__(self):
        super(backgroundThread, self).__init__()
        self.exitPressed = False
        self.spacePressed = False
    def run(self):
        while not self.exitPressed:
            # release and check for ESC
            key = 0xFF
            if key == 27:
            # ESC: quit
                self.exitPressed = True
            if key == 32:
            # space: screenshot
                self.spacePressed = True
                

stream = TwitchStream(
    config.stream_resolution, config.client_id)
screen_classifier = Classifier(config.stream_resolution)
post_match_classifier = Classifier(config.stream_resolution)
screen_classifier.load_templates(
    "templates/screen/*.png", config.template_resolution)
post_match_classifier.load_templates(
    "templates/post_match/*.png", config.template_resolution)

running = True
thread = backgroundThread()
thread.start()

while running:
    frame = stream.get_frame()
    cv2.imshow("frame", frame)
    screen = screen_classifier.classify(frame)
    #running = thread.exitPressed
    if screen is not None:
        post_match_classifier.scale_factor = screen_classifier.scale_factor
        match_result = post_match_classifier.classify_image(frame)
        print("current frame shows screen {} with {}!"
              .format(screen, match_result))
    if thread.spacePressed:
        filename = "{}_{}.png".format(stream.channel, int(time.time()))
        cv2.imwrite(filename, frame)
        thread.spacePressed = False

cv2.destroyAllWindows()
