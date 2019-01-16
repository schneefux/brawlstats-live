#!/usr/bin/env python3
import pytest

from state.enum.screen import Screen
from state.game_state import GameState
from state.stream_config import StreamConfig
from pipe.damage_pipe import DamagePipe

stream_config = StreamConfig(resolution=480,
                             max_fps=0,
                             screen_box=((0, 0), (852, 480)))

def test_should_change_state_on_damage():
    state = GameState(stream_config=stream_config,
                      screen=Screen.GEMGRAB_INGAME)
    pipe = DamagePipe()
    pipe._matcher.classify = lambda *_: True

    changes = pipe.process(None, state)
    assert changes == {
        "taking_damage": True
    }


def test_should_change_state_on_no_damage():
    state = GameState(stream_config=stream_config,
                      screen=Screen.GEMGRAB_INGAME)
    pipe = DamagePipe()
    pipe._matcher.classify = lambda *_: False

    changes = pipe.process(None, state)
    assert changes == {
        "taking_damage": False
    }