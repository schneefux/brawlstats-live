#!/usr/bin/env python3

import cv2
import glob
import config
from classifier import Classifier

def classifier(folder):
    classifier = Classifier(config.stream_resolution)
    classifier.load_templates("templates/{}/*.png".format(folder),
                              config.template_resolution)
    return classifier

def image(path):
    frame = cv2.imread(path)
    print("testing image {}".format(path))
    return frame

def images(*folders):
    for folder in folders:
        for path in glob.glob("test_images/{}/*.png".format(folder)):
            yield image(path)


def test_screen_post_match():
    for frame in images("victory", "defeat"):
        assert classifier("screen").classify(frame) == "post_match"

def test_victory():
    for frame in images("victory"):
        assert classifier("post_match").classify(frame) == "victory"

def test_defeat():
    for frame in images("defeat"):
        assert classifier("post_match").classify(frame) == "defeat"

def test_rank_top():
    for frame in images("rank"):
        assert classifier("post_match").classify(frame) in ["rank", "rank_top"]
def test_unclassified():
    for frame in images("unclassified"):
        assert classifier("screen").classify(frame) == None
        assert classifier("post_match").classify(frame) == None

def test_repeated_classification():
    c = classifier("screen")
    path = "./test_images/victory/phonecats_victory_screenshot.png"
    assert c.classify(image(path)) == "post_match"
    assert c.classify(image(path)) == "post_match"
