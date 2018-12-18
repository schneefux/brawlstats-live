#!/usr/bin/env python3

import cv2
import sys
import config
from classifier import Classifier

classifier = Classifier(config.stream_resolution)
classifier.load_templates("templates/*.png",
                          config.template_resolution)
for path in sys.argv[1:]:
    frame = cv2.imread(path)
    print("{} matches template {}".format(
        path,
        classifier.classify_image(frame)))
