#!/usr/bin/env python3

import cv2
import glob
from state.stream_config import StreamConfig
from classifiers.template_matcher import TemplateMatcher

stream_config = StreamConfig(resolution=480)

def matcher(folder):
    matcher = TemplateMatcher()
    matcher.load_templates("templates/{}/*.png".format(folder),
                           1080, True)
    return matcher

def image(path):
    print("testing image {}".format(path))
    return cv2.imread(path)

def images(*folders):
    for folder in folders:
        for path in glob.glob("test_images/{}/*.png".format(folder)):
            yield image(path)


def test_screen_versus():
    for frame in images("versus"):
        assert matcher("screen")\
            .classify(frame, stream_config)[0] == "versus"

def test_screen_post_match():
    for frame in images("victory", "defeat"):
        assert matcher("screen")\
            .classify(frame, stream_config)[0] == "post_match"

def test_victory():
    for frame in images("victory"):
        assert matcher("post_match")\
            .classify(frame, stream_config)[0] == "victory"

def test_defeat():
    for frame in images("defeat"):
        assert matcher("post_match")\
            .classify(frame, stream_config)[0] == "defeat"

def test_rank_top():
    for frame in images("rank"):
        assert matcher("post_match")\
            .classify(frame, stream_config)[0] in ["rank", "rank_top"]
def test_unclassified():
    for frame in images("unclassified"):
        assert matcher("screen")\
            .classify(frame, stream_config)[0] == None
        assert matcher("post_match")\
            .classify(frame, stream_config)[0] == None

def test_repeated_classification():
    c = matcher("screen")
    path = "./test_images/victory/phonecats_victory_screenshot.png"
    assert c.classify(image(path), stream_config)[0] == "post_match"
    assert c.classify(image(path), stream_config)[0] == "post_match"
