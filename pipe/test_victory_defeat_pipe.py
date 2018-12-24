#!/usr/bin/env python3

import cv2
import glob

from state.game_state import GameState, Screen, MatchResult
from state.stream_config import StreamConfig
from pipe.victory_defeat_pipe import VictoryDefeatPipe

def test_should_classify_result():
    stream_config = StreamConfig(resolution=480,
                                 screen_box=((0, 0), (852, 480)))
    state = GameState(stream_config=stream_config,
                      current_screen=Screen.VICTORY_DEFEAT)
    pipe = VictoryDefeatPipe()
    pipe.start()

    pipe._matcher.classify = lambda *_: [("victory", (0, 0))]

    changes = pipe.process(None, state)

    assert changes["last_match_result"] == MatchResult.VICTORY
    assert changes["stream_config"].template_positions == { "victory": (0, 0) }


def test_should_noop_on_no_match():
    stream_config = StreamConfig(resolution=480,
                                 screen_box=((0, 0), (852, 480)))
    state = GameState(stream_config=stream_config,
                      current_screen=Screen.VICTORY_DEFEAT)
    pipe = VictoryDefeatPipe()
    pipe.start()
    pipe._matcher.classify = lambda *_: []

    changes = pipe.process(None, state)

    assert changes == {}
