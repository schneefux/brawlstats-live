#!/usr/bin/env python3
import cv2
import glob
import pytest

from state.game_state import GameState
from state.enum.screen import Screen
from state.enum.brawler import Brawler
from state.stream_config import StreamConfig
from pipe.versus_pipe import VersusPipe

@pytest.mark.parametrize("data,teams", [
    (
        (
            ('colt', (16, 359)), ('mortis', (18, 617)),
            ('mortis', (333, 242)), ('shelly', (334, 110)),
            ('tara', (19, 490)), ('tara', (335, 368))
        ), (
            (Brawler.COLT, Brawler.TARA, Brawler.MORTIS),
            (Brawler.SHELLY, Brawler.TARA, Brawler.MORTIS)
        )
    ),
    (
        (
            ('colt', (315, 249)), ('jessie', (89, 279)),
            ('leon', (317, 155)), ('nita', (91, 373)),
            ('nita', (318, 60)), ('poco', (90, 465))
        ), (
            (Brawler.JESSIE, Brawler.NITA, Brawler.POCO),
            (Brawler.COLT, Brawler.LEON, Brawler.NITA)
        )
    )
])
def test_should_place_into_teams(data, teams):
    stream_config = StreamConfig(resolution=480,
                                 screen_box=((0, 0), (852, 480)))
    state = GameState(stream_config=stream_config,
                      current_screen=Screen.VERSUS)
    pipe = VersusPipe()
    pipe.start()
    pipe._matcher.classify = lambda *_: data

    changes = pipe.process(None, state)

    assert set(changes["red_team"]) == set(teams[0])
    assert set(changes["blue_team"]) == set(teams[1])


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
