#!/usr/bin/env python3

import cv2
import glob

from state.game_state import GameState, Screen, Brawler
from state.stream_config import StreamConfig
from pipe.versus_pipe import VersusPipe

def assert_lists_same(list1, list2):
    assert all([x in list2 for x in list1])
    assert all([x in list1 for x in list2])

def test_should_recognize_teams():
    stream_config = StreamConfig(resolution=480,
                                 screen_box=((0, 0), (852, 480)))
    state = GameState(stream_config=stream_config,
                      current_screen=Screen.VERSUS)
    pipe = VersusPipe()
    pipe.start()

    image = cv2.imread(
        "test_images/brawler/" +
        "jessie_poco_colt_penny_barley_nita.png")
    changes = pipe.process(image, state)

    assert_lists_same(changes["red_team"],
                      [Brawler.JESSIE, Brawler.POCO, Brawler.COLT])
    assert_lists_same(changes["blue_team"],
                      [Brawler.PENNY, Brawler.BARLEY, Brawler.NITA])
