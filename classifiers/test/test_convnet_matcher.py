#!/usr/bin/env python3
import cv2
import pytest

from state.enum.screen import Screen
from state.stream_config import StreamConfig
from classifiers.convnet_matcher import ConvnetMatcher

from model.screen.config import shape

matcher = ConvnetMatcher(
    image_shape=shape,
    feature_map={screen.value: screen for screen in Screen})
matcher.load_model("model/screen/model.h5")

def image(name):
    frame = cv2.imread("test_images/{}.png".format(name))
    screen_box = ((0, 0),
                  (frame.shape[1], frame.shape[0]))
    stream_config = StreamConfig(resolution=480,
                                 screen_box=screen_box)
    return frame, stream_config


@pytest.mark.parametrize("name,label", [
    ("brawlers_1", "brawlers"),
    ("brawlers_2", "brawlers"),
    ("chest_1", "chest"),
    ("choose-event_1", "choose_event"),
    #("defeat_1", "defeat"),
    ("defeat_2", "defeat"),
    #("defeat_3", "defeat"),
    ("defeat_4", "defeat"),
    #("friendslist_1", "friendslist"),
    #("ingame_1", None),
    #("ingame_2", None),
    #("ingame_3", None),
    #("ingame_4", None),
    #("ingame_5", None),
    #("ingame_6", None),
    #("ingame_7", None),
    #("ingame-solo-showdown_1", None),
    #("ingame-brawlball_1", None),
    ("loading_1", "loading"),
    ("loading_2", "loading"),
    ("loading_3", "loading"),
    #("main-menu_1", "main_menu"),
    #("main-menu_2", "main_menu"),
    #("main-menu_3", "main_menu"),
    ("main-menu-team_1", "main_menu_team"),
    #("main-menu-team_2", "main_menu_team"),
    #("main-menu-team_3", "main_menu_team"),
    ("mode-gem-grab_1", "mode_gem_grab"),
    #("other_1", None),
    ("play-again_1", "play_again"),
    ("play-again_2", "play_again"),
    ("play-again_3", "play_again"),
    ("play-again_4", "play_again"),
    ("play-again_5", "play_again"),
    ("play-again_6", "play_again"),
    ("play-again_7", "play_again"),
    ("play-again_8", "play_again"),
    ("play-again_9", "play_again"),
    ("queue_1", "queue"),
    ("queue_2", "queue"),
    ("queue_3", "queue"),
    ("queue_4", "queue"),
    ("queue_5", "queue"),
    ("queue_6", "queue"),
    ("queue_7", "queue"),
    ("queue_8", "queue"),
    ("queue_9", "queue"),
    ("rank_1", "rank"),
    ("rank_2", "rank"),
    ("rank_3", "rank"),
    ("rank_4", "rank"),
    #("select-brawler_1", "select_brawler"),
    #("versus_colt-tara-mortis-shelly-mortis-tara", "versus"),
    #("versus_frank-colt-nita-nita-tara-shelly", "versus"),
    #("versus_frank-poco-nita-jessie-nita-pam", "versus"),
    #("versus_nita-shelly-crow-brock-colt-frank", "versus"),
    #("versus_shelly-bull-barley-nita-poco-penny", "versus"),
    #("versus_nita-brock-colt-colt-ricochet-jessie", "versus"),
    ("victory_1", "victory"),
    ("victory_2", "victory"),
    ("victory_3", "victory"),
    ("victory_4", "victory"),
    ("victory_5", "victory"),
    ("victory_6", "victory"),
    ("victory_7", "victory"),
    ("victory_8", "victory"),
])
def test_screen(name, label):
    labels = [Screen[label.upper()]] if label is not None else []
    assert [r[0] for r in matcher.classify(*image(name))] == labels
