#!/usr/bin/env python3

import cv2
import sys
import config
from state.stream_config import StreamConfig
from classifiers.template_matcher import TemplateMatcher
from classifiers.multi_template_matcher import MultiTemplateMatcher

# TODO screen box is hardcoded
stream_config = StreamConfig(resolution=480,
                             screen_box=((0, 0), (852, 480)))

def matcher(folder):
    matcher = TemplateMatcher()
    matcher.load_templates("templates/{}/*.png".format(folder),
                           1080)
    return matcher

def mmatcher(folder):
    matcher = MultiTemplateMatcher()
    matcher.load_templates("templates/{}/*.png".format(folder),
                           1080)
    return matcher

if __name__ == "__main__":
    for path in sys.argv[1:]:
        frame = cv2.imread(path)
        screen_label = matcher("screen")\
            .classify(frame, stream_config)[0]
        result_label = matcher("victory_defeat")\
            .classify(frame, stream_config)[0]
        brawlers = [b[0] for b in mmatcher("brawler")\
                    .classify(frame, stream_config)]
        print("{} shows screen {} with {} and {}!"
              .format(path, screen_label, result_label, brawlers))
