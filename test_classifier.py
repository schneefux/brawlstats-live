#!/usr/bin/env python3

import cv2
import glob
import config
from classifier import Classifier

screen_classifier = Classifier(config.stream_resolution)
post_match_classifier = Classifier(config.stream_resolution)
screen_classifier.load_templates(
    "templates/screens/*.png", config.template_resolution)
post_match_classifier.load_templates(
    "templates/post_match/*.png", config.template_resolution)

def load_test_images(*folders):
    for folder in folders:
        for path in glob.glob("{}/*.png".format(folder)):
            frame = cv2.imread(path)
            yield frame


def test_screen_post_match():
    for frame in load_test_images("victory", "defeat"):
        assert screen_classifier.classify_image(frame) == "post_match"

def test_victory():
    for frame in load_test_images("victory"):
        assert post_match_classifier.classify_image(frame) == "victory"

def test_defeat():
    for frame in load_test_images("defeat"):
        assert post_match_classifier.classify_image(frame) == "defeat"

def test_unclassified():
    for frame in load_test_images("unclassified"):
        assert screen_classifier.classify_image(frame) == None
        assert post_match_classifier.classify_image(frame) == None
