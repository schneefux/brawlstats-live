#!/usr/bin/env python3
import cv2
import pytest

from state.stream_config import StreamConfig
from matcher.gembar_matcher import BlueGembarMatcher, RedGembarMatcher

def image(name):
    frame = cv2.imread("test_images/{}.png".format(name))
    screen_box = ((0, 0),
                  (frame.shape[1], frame.shape[0]))
    stream_config = StreamConfig(resolution=480,
                                 max_fps=0,
                                 screen_box=screen_box)
    return frame, stream_config


@pytest.mark.parametrize("name,percentage", [
    ("ingame_3", 0.6),
    ("ingame_4", 1.0),
    ("ingame_6", 1.0),
    ("ingame_9", 0.2),
    ("ingame_10", 0.4),
    ("ingame_11", 0.3),
    ("ingame_12", 0.6),
    ("ingame_14", 0.4),
])
def test_gembar_blue(name, percentage):
    assert round(BlueGembarMatcher().classify(*image(name)), 1) == percentage

    
@pytest.mark.parametrize("name,percentage", [
    ("ingame_3", 0.7),
    ("ingame_4", 0.0),
    ("ingame_9", 0.1),
    ("ingame_10", 0.1),
    ("ingame_12", 1.0),
    ("ingame_14", 0.2),
])
def test_gembar_red(name, percentage):
    assert round(RedGembarMatcher().classify(*image(name)), 1) == percentage

    
def test_no_gembar():
    assert RedGembarMatcher().classify(*image("loading_1")) == None
    assert BlueGembarMatcher().classify(*image("loading_1")) == None


def test_ignore_gembar_flash():
    assert BlueGembarMatcher().classify(*image("ingame_13")) == None