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
                           1920, 1080)
    return matcher

def image(name):
    frame = cv2.imread("test_images/{}.png".format(name))
    screen_box = ((0, 0),
                  (frame.shape[1], frame.shape[0]))
    stream_config = StreamConfig(resolution=480,
                                 screen_box=screen_box)
    return frame, stream_config


@pytest.mark.parametrize("name,label", [
    #("brawlers_1", "brawlers"), # cut off
    ("chest_1", "chest"),
    ("choose-event_1", "choose_event"),
    ("defeat_1", "victory_defeat"),
    ("defeat_2", "victory_defeat"),
    #("defeat_3", "victory_defeat"), # skewed
    ("defeat_4", "victory_defeat"),
    ("friendslist_1", "friendslist"),
    ("ingame_1", None),
    ("ingame_2", None),
    ("ingame_3", None),
    ("ingame_4", None),
    ("ingame_5", None),
    ("ingame_6", None),
    ("ingame_7", None),
    ("ingame-brawlball_1", None),
    ("loading_1", "loading"),
    ("loading_2", "loading"),
    ("loading_3", "loading"),
    ("main-menu_1", "main_menu"),
    #("main-menu_2", "main_menu"), # bad quality
    ("main-menu_3", "main_menu"),
    ("main-menu-team_1", "main_menu_team"),
    ("main-menu-team_2", "main_menu_team"),
    ("main-menu-team_3", "main_menu_team"),
    #("other_1", None), # ?
    #("play-again_1", "play_again"), # skewed
    ("play-again_2", "play_again"),
    ("play-again_3", "play_again"),
    ("play-again_4", "play_again"),
    ("play-again_5", "play_again"),
    ("play-again_6", "play_again"),
    ("play-again_7", "play_again"),
    ("play-again_8", "play_again"),
    #("play-again_9", "play_again"), # cut off
    ("queue_1", "queue"),
    #("queue_2", "queue"), # ?
    ("queue_3", "queue"),
    #("queue_4", "queue"), # missing button
    #("queue_5", "queue"), # covered by text
    ("queue_6", "queue"),
    #("queue_7", "queue"), # covered by icon
    ("queue_8", "queue"),
    #("queue_9", "queue"), # no button
    ("rank_1", "victory_defeat"),
    #("rank_2", "victory_defeat"), # covered by text
    ("rank_3", "victory_defeat"),
    ("rank_4", "victory_defeat"),
    #("rank_team_1", "victory_defeat"), # skewed
    ("select-brawler_1", "select_brawler"),
    #("versus_colt-tara-mortis-shelly-mortis-tara", "versus"), # ?
    ("versus_frank-colt-nita-nita-tara-shelly", "versus"),
    ("versus_frank-poco-nita-jessie-nita-pam", "versus"),
    ("versus_nita-shelly-crow-brock-colt-frank", "versus"),
    ("versus_shelly-bull-barley-nita-poco-penny", "versus"),
    ("versus_nita-brock-colt-colt-ricochet-jessie", "versus"),
    ("victory_1", "victory_defeat"),
    ("victory_2", "victory_defeat"),
    ("victory_3", "victory_defeat"),
    ("victory_4", "victory_defeat"),
    #("victory_5", "victory_defeat"), # covered by head
    ("victory_6", "victory_defeat"),
    ("victory_7", "victory_defeat"),
])
def test_screen(name, label):
    labels = [label] if label is not None else []
    assert [r[0] for r in matcher("screen")\
        .classify(*image(name), True)] == labels


@pytest.mark.parametrize("name,label", [
    ("defeat_1", "defeat"),
    ("defeat_2", "defeat"),
    #("defeat_3", "defeat"), # skewed
    ("victory_1", "victory"),
    ("victory_2", "victory"),
    ("victory_3", "victory"),
    #("victory_4", "victory"), # skewed
    #("victory_5", "victory"), # ?
    ("rank_1", "rank"),
    ("rank_2", "rank"),
    ("rank_3", "rank_top"),
    ("rank_4", "rank"),
])
def test_victory_defeat(name, label):
    assert [r[0] for r in matcher("victory_defeat")\
        .classify(*image(name), True)] == [label]


@pytest.mark.parametrize("name,labels", [
    ("versus_colt-tara-mortis-shelly-mortis-tara", ["colt", "tara", "mortis", "shelly", "mortis", "tara"]),
    ("versus_frank-colt-nita-nita-tara-shelly", ["frank", "colt", "nita", "nita", "tara", "shelly"]),
    ("versus_frank-poco-nita-jessie-nita-pam", ["frank", "poco", "nita", "jessie", "nita", "pam"]),
    ("versus_shelly-bull-barley-nita-poco-penny", ["shelly", "bull", "barley", "nita", "poco", "penny"]),
    ("versus_nita-shelly-crow-brock-colt-frank", ["nita", "shelly", "crow", "brock", "colt", "frank"]),
    ("versus_nita-brock-colt-colt-ricochet-jessie", ["nita", "brock", "colt", "colt", "ricochet", "jessie"]),
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
