#!/usr/bin/env python3

import cv2
import sys
import config
from classifier import Classifier

def classifier(folder):
    classifier = Classifier(config.stream_resolution)
    classifier.load_templates("templates/{}/*.png".format(folder),
                              config.template_resolution)
    return classifier

for path in sys.argv[1:]:
    frame = cv2.imread(path)
    screen = classifier("screen").classify(frame)
    match_result = classifier("post_match").classify(frame)
    print("{} shows screen {} with {}!"
          .format(path, screen, match_result))
