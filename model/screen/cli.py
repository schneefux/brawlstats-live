#!/usr/bin/env python3
import cv2
import sys
import numpy as np
from keras.models import load_model
from keras.backend import image_data_format

IMAGE_SHAPE = (10, 10)
INDICES = {'showdown_defeated': 24, 'trophyroad': 31, 'profile': 20, 'brawlers': 1, 'showdown_ingame': 26, 'heist_end': 11, 'queue': 21, 'rank': 22, 'showdown_solo_start': 28, 'main_menu': 17, 'club': 4, 'chest': 2, 'gemgrab_end': 7, 'play_again': 19, 'heist_start': 13, 'invite': 15, 'loading': 16, 'showdown_showdown': 27, 'gemgrab_start': 9, 'showdown_wait_respawn': 30, 'event_info': 6, 'heist_wait_respawn': 14, 'showdown_wait_ally_respawn': 29, 'heist_ingame': 12, 'gemgrab_ingame': 8, 'defeat': 5, 'gemgrab_wait_respawn': 10, 'victory': 33, 'choose_event': 3, 'battle_log': 0, 'main_menu_team': 18, 'showdown_duo_start': 25, 'versus': 32, 'select_brawler': 23}
feature_map = {v: k for k, v in INDICES.items()}

model = load_model("model.h5")

for path in sys.argv[1:]:
    frame = cv2.imread(path)
    frame = cv2.resize(frame, IMAGE_SHAPE)
    
    if image_data_format() == "channels_first":
        # cv2 is channel last, keras+theano is channels first
        frame = np.moveaxis(frame, -1, 0)

    # cv2 bgr to keras rgb
    frame = frame[::-1]
    # cv2 int to keras float
    frame = frame.astype(np.float32)
    frame = frame.reshape((1, ) + frame.shape)

    feature_vector = model.predict(frame)[0]
    matches = [(feature_map[i], feature_vector[i])
            for i in range(len(feature_vector))
            if feature_vector[i] > 0.1]
    for label, confidence in matches:
        print("{}: {} ({}%)".format(path, label, int(100*confidence)))
