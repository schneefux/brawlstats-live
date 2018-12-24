#!/usr/bin/env python3

import cv2
import sys
import config
from state.stream_config import StreamConfig
from classifiers.template_matcher import TemplateMatcher

def matcher(folder):
    matcher = TemplateMatcher()
    matcher.load_templates("templates/{}/*.png".format(folder),
                           1080)
    return matcher

if __name__ == "__main__":
    for path in sys.argv[1:]:
        frame = cv2.imread(path)
        stream_config = StreamConfig(
            resolution=480,
            screen_box=((0, 0), (frame.shape[1], frame.shape[0])))

        screen_labels  = [s[0] for s in matcher("screen")\
            .classify(frame, stream_config)]
        result_labels  = [r[0] for r in matcher("victory_defeat")\
            .classify(frame, stream_config)]
        brawler_labels = [b[0] for b in matcher("brawler")\
            .classify(frame, stream_config)]
        print("{} shows screen {} with {} and {}!".format(
            path, screen_labels, result_labels, brawler_labels))
        print(matcher("brawler").classify(frame, stream_config))
