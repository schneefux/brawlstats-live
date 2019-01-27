#!/usr/bin/env python3

import cv2
import glob

from state.game_state import GameState
from state.enum.screen import Screen
from state.enum.brawler import Brawler
from state.stream_config import StreamConfig
from pipe.screen_pipe import ScreenPipe

stream_config = StreamConfig(resolution=480,
                             max_fps=0,
                             screen_box=((0, 0), (852, 480)))

def test_should_change_screen_on_no_match():
    state = GameState(stream_config=stream_config, screen=None)
    pipe = ScreenPipe()

    pipe._matcher.classify = lambda *_: []

    changes = pipe.process(None, state)
    assert changes == {
        "screen": None
    }


def test_should_set_last_queue():
    state = GameState(stream_config=stream_config,
                      screen=None,
                      timestamp=1234)
    pipe = ScreenPipe()

    pipe._matcher.classify = lambda *_: [(Screen.QUEUE, 1.0)]

    changes = pipe.process(None, state)
    assert changes == {
        "screen": Screen.QUEUE,
        "last_queue": 1234
    }


def test_should_change_screen_on_match():
    state = GameState(stream_config=stream_config, screen=None)
    pipe = ScreenPipe()

    pipe._matcher.classify = lambda *_: [(Screen.LOADING, 1.0)]

    changes = pipe.process(None, state)
    assert changes == {
        "screen": Screen.LOADING
    }
