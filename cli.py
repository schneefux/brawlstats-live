#!/usr/bin/env python3

import cv2
import sys
import classifier

for path in sys.argv[1:]:
    frame = cv2.imread(path)
    print("{} matches template {}".format(
        path,
        classifier.classify_image(frame)))
