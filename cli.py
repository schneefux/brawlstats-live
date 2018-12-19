#!/usr/bin/env python3

import cv2
import sys
import config
from classifier import Classifier

screen_classifier = Classifier(config.stream_resolution)
post_match_classifier = Classifier(config.stream_resolution)
screen_classifier.load_templates(
    "templates/screens/*.png", config.template_resolution)
post_match_classifier.load_templates(
    "templates/post_match/*.png", config.template_resolution)
for path in sys.argv[1:]:
    frame = cv2.imread(path)
    screen = screen_classifier.classify(frame)
    if screen is not None:
        match_result = post_match_classifier.classify(frame)
        print("current frame shows screen {} with {}!"
              .format(screen, match_result))
