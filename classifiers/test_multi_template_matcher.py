#!/usr/bin/env python3

import cv2
import glob

from state.stream_config import StreamConfig
from classifiers.multi_template_matcher import MultiTemplateMatcher

def matcher(folder):
    matcher = MultiTemplateMatcher()
    matcher.load_templates("templates/{}/*.png".format(folder),
                           1080)
    return matcher

def image(path):
    print("testing image {}".format(path))
    return cv2.imread(path)


def test_loading_screen_brawlers_1():
    stream_config = StreamConfig(resolution=480,
                                 aspect_ratio_factor=1.0)
    matches = matcher("brawler").classify(
        image("test_images/brawler/" +
              "jessie_poco_colt_penny_barley_nita.png"),
        stream_config)
    brawlers = [match[0] for match in matches]
    assert "jessie" in brawlers
    assert "poco" in brawlers
    assert "colt" in brawlers
    assert "penny" in brawlers
    assert "barley" in brawlers
    assert "nita" in brawlers
    assert len(brawlers) == 6

def test_loading_screen_brawlers_2():
    stream_config = StreamConfig(resolution=480,
                                 aspect_ratio_factor=1.36)
    matches = matcher("brawler").classify(
        image("test_images/brawler/" +
              "frank_poco_nita_jessie_nita_pam.png"),
        stream_config)
    brawlers = [match[0] for match in matches]
    # TODO: Add missing templates
    #assert "frank" in brawlers
    assert "poco" in brawlers
    assert "nita" in brawlers
    assert "jessie" in brawlers
    #assert "pam" in brawlers
    #assert len(brawlers) == 6
    assert len(brawlers) == 4
