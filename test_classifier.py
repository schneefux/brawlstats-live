#!/usr/bin/env python3

import cv2
import glob
import config
from classifier import Classifier

TEMPLATES = ["screen", "post_match"]

classifier = dict()
for name in TEMPLATES:
    classifier[name] = Classifier(config.stream_resolution)
    classifier[name].load_templates(
        "templates/{}/*.png".format(name), config.template_resolution)

def images(*folders):
    for folder in folders:
        for path in glob.glob("test_images/{}/*.png".format(folder)):
            frame = cv2.imread(path)
            yield frame


def test_screen_post_match():
    for frame in images("victory", "defeat"):
        assert classifier["screen"].classify(frame) == "post_match"

def test_victory():
    for frame in images("victory"):
        assert classifier["post_match"].classify(frame) == "victory"

def test_defeat():
    for frame in images("defeat"):
        assert classifier["post_match"].classify(frame) == "defeat"

def test_unclassified():
    for frame in images("unclassified"):
        assert classifier["screen"].classify(frame) == None
        assert classifier["post_match"].classify(frame) == None
