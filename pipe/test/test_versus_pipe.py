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
            ('colt', (359, 16)), ('mortis', (617, 18)),
            ('mortis', (242, 333)), ('shelly', (110, 334)),
            ('tara', (490, 19)), ('tara', (368, 335))
        ), (
            (Brawler.COLT, Brawler.TARA, Brawler.MORTIS),
            (Brawler.SHELLY, Brawler.TARA, Brawler.MORTIS)
        )
    ),
    (
        (
            ('colt', (249, 315)), ('jessie', (279, 89)),
            ('leon', (155, 317)), ('nita', (373, 91)),
            ('nita', (60, 318)), ('poco', (465, 90))
        ), (
            (Brawler.JESSIE, Brawler.NITA, Brawler.POCO),
            (Brawler.COLT, Brawler.LEON, Brawler.NITA)
        )
    )
])
def test_should_place_into_teams(data, teams):
    stream_config = StreamConfig(resolution=480,
                                 max_fps=0,
                                 screen_box=((10, 10), (842, 470)))
    state = GameState(stream_config=stream_config,
                      screen=Screen.GEMGRAB_VERSUS)
    pipe = VersusPipe()
    pipe.start()
    pipe._matcher.classify = lambda *_: data

    changes = pipe.process(None, state)

    assert set(changes["red_team"]) == set(teams[0])
    assert set(changes["blue_team"]) == set(teams[1])


def test_should_noop_on_too_few_brawlers():
    stream_config = StreamConfig(resolution=480,
                                 max_fps=0,
                                 screen_box=((10, 10), (842, 470)))
    state = GameState(stream_config=stream_config,
                      screen=Screen.GEMGRAB_VERSUS)
    pipe = VersusPipe()
    pipe.start()
    pipe._matcher.classify = lambda *_: (
        ('colt', (249, 315)), ('jessie', (279, 89)),
        ('leon', (155, 317)), ('nita', (373, 91)))

    changes = pipe.process(None, state)

    assert changes == {}


def test_should_noop_on_no_match(monkeypatch):
    stream_config = StreamConfig(resolution=480,
                                 max_fps=0,
                                 screen_box=((10, 10), (842, 470)))
    state = GameState(stream_config=stream_config,
                      screen=Screen.GEMGRAB_VERSUS)
    pipe = VersusPipe()
    pipe.start()
    monkeypatch.setattr(cv2, "imwrite", lambda *_: None)
    pipe._matcher.classify = lambda *_: []

    changes = pipe.process(None, state)

    assert changes == {}


def test_should_reset_on_play_again():
    stream_config = StreamConfig(resolution=480,
                                 max_fps=0,
                                 screen_box=((10, 10), (842, 470)))
    state = GameState(stream_config=stream_config,
                      screen=Screen.PLAY_AGAIN,
                      blue_team=[Brawler.RICOCHET, Brawler.NITA, Brawler.LEON],
                      red_team=[Brawler.RICOCHET, Brawler.BO, Brawler.BROCK])
    pipe = VersusPipe()
    pipe.start()

    changes = pipe.process(None, state)

    assert changes == {
        "blue_team": [],
        "red_team": []
    }


def test_should_noop_on_existing_team():
    stream_config = StreamConfig(resolution=480,
                                 max_fps=0,
                                 screen_box=((10, 10), (842, 470)))
    state = GameState(stream_config=stream_config,
                      screen=Screen.GEMGRAB_VERSUS,
                      blue_team=[Brawler.RICOCHET, Brawler.NITA, Brawler.LEON],
                      red_team=[Brawler.RICOCHET, Brawler.BO, Brawler.BROCK])
    pipe = VersusPipe()
    pipe.start()

    changes = pipe.process(None, state)

    assert changes == {}
