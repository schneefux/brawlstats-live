#!/usr/bin/env python3

import cv2
import glob

from state.game_state import GameState, Screen, Brawler
from state.stream_config import StreamConfig
from pipe.screen_pipe import ScreenPipe

stream_config = StreamConfig(resolution=480,
                             screen_box=((0, 0), (852, 480)))

def test_should_search_start_and_find_none():
    state = GameState(stream_config=stream_config,
                      last_known_screen=None,
                      current_screen=None)
    pipe = ScreenPipe()
    pipe.start()

    pipe._matchers[Screen.VERSUS].classify = lambda *_: []
    pipe._matchers[Screen.LOADING].classify = lambda *_: []

    changes = pipe.process(None, state)
    assert changes == {}


def test_should_search_start_and_find():
    state = GameState(stream_config=stream_config,
                      last_known_screen=None,
                      current_screen=None)
    pipe = ScreenPipe()
    pipe.start()

    pipe._matchers[Screen.VERSUS].classify = \
        lambda *_: [("versus", (0, 0))]
    pipe._matchers[Screen.LOADING].classify = lambda *_: []

    changes = pipe.process(None, state)
    assert changes["current_screen"] == Screen.VERSUS
    assert changes["last_known_screen"] == Screen.VERSUS
    assert changes["stream_config"].template_positions == { "versus": (0, 0) }


def test_should_search_same_and_find_none():
    state = GameState(stream_config=stream_config,
                      last_known_screen=Screen.VERSUS,
                      current_screen=Screen.VERSUS)
    pipe = ScreenPipe()
    pipe.start()

    pipe._matchers[Screen.VERSUS].classify = lambda *_: []

    changes = pipe.process(None, state)
    assert changes["current_screen"] == None
    assert changes["last_known_screen"] == Screen.VERSUS


def test_should_search_same_and_find():
    state = GameState(stream_config=stream_config,
                      last_known_screen=Screen.VERSUS,
                      current_screen=Screen.VERSUS)
    pipe = ScreenPipe()
    pipe.start()

    pipe._matchers[Screen.VERSUS].classify = \
        lambda *_: [("versus", (0, 0))]

    changes = pipe.process(None, state)
    assert changes == {}


def test_should_search_next_and_find_none():
    state = GameState(stream_config=stream_config,
                      last_known_screen=Screen.VERSUS,
                      current_screen=None)
    pipe = ScreenPipe()
    pipe.start()

    pipe._matchers[Screen.VICTORY_DEFEAT].classify = lambda *_: []

    changes = pipe.process(None, state)
    assert changes == {}


def test_should_search_next_and_find():
    state = GameState(stream_config=stream_config,
                      last_known_screen=Screen.VERSUS,
                      current_screen=None)
    pipe = ScreenPipe()
    pipe.start()

    pipe._matchers[Screen.VICTORY_DEFEAT].classify = \
        lambda *_: [("victory_defeat", (0, 0))]

    changes = pipe.process(None, state)
    assert changes["current_screen"] == Screen.VICTORY_DEFEAT
    assert changes["last_known_screen"] == Screen.VICTORY_DEFEAT
    assert changes["stream_config"].template_positions == { "victory_defeat": (0, 0) }
