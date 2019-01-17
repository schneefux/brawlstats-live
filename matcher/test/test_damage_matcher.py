#!/usr/bin/env python3
import cv2
import pytest

from state.stream_config import StreamConfig
from matcher.damage_matcher import DamageMatcher

def image(name):
    frame = cv2.imread("test_images/{}.png".format(name))
    screen_box = ((0, 0),
                  (frame.shape[1], frame.shape[0]))
    stream_config = StreamConfig(resolution=480,
                                 max_fps=0,
                                 screen_box=screen_box)
    return frame, stream_config


@pytest.mark.parametrize("name,matches", [
    ("ingame_1", False),
    ("ingame_2", False),
    ("ingame_3", False),
    ("ingame_4", False),
    ("ingame_5", True),
    ("ingame_6", False),
])
def test_damage(name, matches):
    assert DamageMatcher()\
        .classify(*image(name)) == matches