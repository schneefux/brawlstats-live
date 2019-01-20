#!/usr/bin/env python3
from state.game_state import GameState
from state.stream_config import StreamConfig
from pipe.debug_pipe import DebugPipe

def test_not_throw_error():
    state = GameState(
        timestamp=0,
        stream_config=StreamConfig(resolution=0, max_fps=0))
    sink = DebugPipe()
    sink.start()
    sink.process(None, state)