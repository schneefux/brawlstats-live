#!/usr/bin/env python3
import cv2
import pytest
from attr import evolve

from state.stream_config import StreamConfig
from classifiers.template_matcher import TemplateMatcher

def matcher(label):
    matcher = TemplateMatcher()
    matcher.load_templates("templates/{}/*.png".format(label),
                           1920, 1080)
    return matcher

def image(name):
    frame = cv2.imread("test_images/{}.png".format(name))
    screen_box = ((0, 0),
                  (frame.shape[1], frame.shape[0]))
    stream_config = StreamConfig(resolution=480,
                                 screen_box=screen_box)
    return frame, stream_config


@pytest.mark.parametrize("name,labels", [
    ("versus_colt-tara-mortis-shelly-mortis-tara", ["colt", "tara", "mortis", "shelly", "mortis", "tara"]),
    ("versus_frank-colt-nita-nita-tara-shelly", ["frank", "colt", "nita", "nita", "tara", "shelly"]),
    ("versus_frank-poco-nita-jessie-nita-pam", ["frank", "poco", "nita", "jessie", "nita", "pam"]),
    ("versus_shelly-bull-barley-nita-poco-penny", ["shelly", "bull", "barley", "nita", "poco", "penny"]),
    ("versus_nita-shelly-crow-brock-colt-frank", ["nita", "shelly", "crow", "brock", "colt", "frank"]),
    ("versus_nita-brock-colt-colt-ricochet-jessie", ["nita", "brock", "colt", "colt", "ricochet", "jessie"]),
])
def test_brawlers(name, labels):
    assert set(r[0] for r in matcher("brawler")\
	.classify(*image(name))) == set(labels)


def test_with_cached_position():
    m = matcher("brawler")
    frame = image("versus_colt-tara-mortis-shelly-mortis-tara")[0]

    screen_box = ((8, 8), (frame.shape[1]-8, frame.shape[0]-8))
    stream_config = StreamConfig(resolution=480, screen_box=screen_box)

    # first classification
    label, position = m.classify(frame, stream_config)[0]
    assert label == "colt"

    # again with cached position
    stream_config = evolve(stream_config, template_positions = {
	label: position
    })
    assert m.classify(frame, stream_config)[0] == (label, position)

    # again with cached position, but box is shifted by 10px
    screen_box = ((16, 16), (frame.shape[1], frame.shape[0]))
    stream_config = StreamConfig(resolution=480, screen_box=screen_box)
    assert m.classify(frame, stream_config)[0] == (label, position)
