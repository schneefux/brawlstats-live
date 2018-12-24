#!/usr/bin/env python3

import cv2
import glob
import pytest
from attr import evolve

from state.stream_config import StreamConfig
from classifiers.template_matcher import TemplateMatcher

def assert_lists_same(list1, list2):
    assert all([x in list2 for x in list1])
    assert all([x in list1 for x in list2])

def matcher(label):
    matcher = TemplateMatcher()
    matcher.load_templates("templates/{}/*.png".format(label),
                           1080)
    return matcher

def image(name):
    frame = cv2.imread("test_images/{}.png".format(name))
    screen_box = ((0, 0),
                  (frame.shape[1], frame.shape[0]))
    stream_config = StreamConfig(resolution=480,
                                 screen_box=screen_box)
    return frame, stream_config


@pytest.mark.parametrize("name,label", [
    ("defeat_1", "victory_defeat"),
    #("defeat_2", "victory_defeat"),
    #("defeat_3", "victory_defeat"),
    ("victory_1", "victory_defeat"),
    #("victory_2", "victory_defeat"),
    ("victory_3", "victory_defeat"),
    ("victory_4", "victory_defeat"),
    #("victory_5", "victory_defeat"),
    #("rank_1", "victory_defeat"),
    #("rank_2", "victory_defeat"),
    #("versus_colt_tara_mortis_shelly_mortis_tara", "versus"),
    #("versus_frank_colt_nita_nita_tara_shelly", "versus"),
    #("versus_frank_poco_nita_jessie_nita_pam", "versus"),
    ("versus_shelly_bull_barley_nita_poco_penny", "versus"),
    #("loading_1", "loading"),
    ("queue_1", "queue"),
    #("queue_2", "queue"),
    #("main-menu_1", "main_menu"),
    ("ingame_1", None),
    ("ingame_2", None),
    ("ingame_3", None),
    ("ingame_4", None),
    ("ingame_5", None),
    ("ingame_6", None),
])
def test_screen(name, label):
    labels = [label] if label is not None else []
    assert [r[0] for r in matcher("screen")\
        .classify(*image(name))] == labels


@pytest.mark.parametrize("name,label", [
    ("defeat_1", "defeat"),
    #("defeat_2", "defeat"),
    #("defeat_3", "defeat"),
    ("victory_1", "victory"),
    #("victory_2", "victory"),
    ("victory_3", "victory"),
    #("victory_4", "victory"),
    #("victory_5", "victory"),
    ("rank_1", "rank"),
    #("rank_2", "rank"),
])
def test_victory_defeat(name, label):
    assert [r[0] for r in matcher("victory_defeat")\
        .classify(*image(name))] == [label]


@pytest.mark.parametrize("name,labels", [
    ("versus_colt_tara_mortis_shelly_mortis_tara", ["colt", "tara", "mortis", "shelly", "mortis", "tara"]),
    #("versus_frank_colt_nita_nita_tara_shelly", ["frank", "colt", "nita", "nita", "tara", "shelly"]),
    #("versus_frank_poco_nita_jessie_nita_pam", ["frank", "poco", "nita", "jessie", "nita", "pam"]),
    ("versus_shelly_bull_barley_nita_poco_penny", ["shelly", "bull", "barley", "nita", "poco", "penny"]),
])
def test_brawlers(name, labels):
    assert set(r[0] for r in matcher("brawler")\
	.classify(*image(name))) == set(labels)


def test_with_cached_position():
    m = matcher("screen")
    frame, stream_config = image("victory_1")
    label, position = m.classify(frame, stream_config)[0]
    stream_config = evolve(stream_config, template_positions = {
	"victory": position
    })
    assert m.classify(frame, stream_config)[0] == (label, position)
