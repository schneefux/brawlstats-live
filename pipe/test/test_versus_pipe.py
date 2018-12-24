#!/usr/bin/env python3

import cv2
import glob

from state.game_state import GameState, Screen, Brawler
from state.stream_config import StreamConfig
from pipe.versus_pipe import VersusPipe

def test_should_place_into_teams():
    stream_config = StreamConfig(resolution=480,
                                 screen_box=((0, 0), (852, 480)))
    state = GameState(stream_config=stream_config,
                      current_screen=Screen.VERSUS)
    pipe = VersusPipe()
    pipe.start()
    result = [
        ('colt', (14, 359)), ('shelly', (333, 110)),
        ('tara', (19, 488)), ('tara', (334, 369)),
        ('mortis', (17, 617)), ('mortis', (332, 241))]
    pipe._matcher.classify = lambda *_: result

    changes = pipe.process(None, state)

    assert set(changes["red_team"]) == set([
        Brawler.COLT, Brawler.TARA, Brawler.MORTIS])
    assert set(changes["blue_team"]) == set([
        Brawler.SHELLY, Brawler.TARA, Brawler.MORTIS])


def test_should_noop_on_no_match(monkeypatch):
    stream_config = StreamConfig(resolution=480,
                                 screen_box=((0, 0), (852, 480)))
    state = GameState(stream_config=stream_config,
                      current_screen=Screen.VERSUS)
    pipe = VersusPipe()
    pipe.start()
    monkeypatch.setattr(cv2, "imwrite", lambda *_: None)
    pipe._matcher.classify = lambda *_: []

    changes = pipe.process(None, state)

    assert changes == {}
