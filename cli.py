#!/usr/bin/env python3

import cv2
import sys
import config
from state.stream_config import StreamConfig
from classifiers.template_matcher import TemplateMatcher

stream_config = StreamConfig(resolution=480, aspect_ratio_factor=None)

def matcher(folder):
    matcher = TemplateMatcher()
    matcher.load_templates("templates/{}/*.png".format(folder),
                           1080, True)
    return matcher

if __name__ == "__main__":
    for path in sys.argv[1:]:
        frame = cv2.imread(path)
        screen = matcher("screen").classify(frame, stream_config)[0]
        match_result = matcher("post_match").classify(frame, stream_config)[0]
        print("{} shows screen {} with {}!"
              .format(path, screen, match_result))
