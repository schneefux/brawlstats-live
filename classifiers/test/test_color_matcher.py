#!/usr/bin/env python3
import cv2
import pytest

from state.stream_config import StreamConfig
from classifiers.color_matcher import ColorMatcher, ColorRange

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
    assert ColorMatcher(ColorRange.DAMAGE())\
        .classify(*image(name))[0] == matches
    

@pytest.mark.parametrize("name,percentage", [
    ("ingame_3", 0.6),
    ("ingame_4", 1.0),
    ("ingame_5", 0.0),
    ("ingame_6", 1.0),
])
def test_gembar_blue(name, percentage):
    assert round(ColorMatcher(ColorRange.GEMBAR_BLUE())\
        .classify(*image(name))[1], 1) == percentage

    
@pytest.mark.parametrize("name,percentage", [
    ("ingame_3", 0.7),
    ("ingame_4", 0.0),
    ("ingame_5", 0.4),
    ("ingame_6", 0.3),
])
def test_match(name, percentage):
    assert round(ColorMatcher(ColorRange.GEMBAR_RED())\
        .classify(*image(name))[1], 1) == percentage

    