import cv2
import sys
import numpy as np
from keras.models import load_model
from keras.backend import image_data_format

IMAGE_SHAPE = (100, 100)
INDICES = {'mode_gem_grab': 7, 'brawlers': 0, 'choose_event': 2, 'main_menu_team': 6, 'victory': 13, 'chest': 1, 'rank': 11, 'queue': 10, 'main_menu': 5, 'play_again': 9, 'defeat': 3, 'mode_solo_showdown': 8, 'loading': 4, 'versus': 12}
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
    best_match_index = np.argmax(feature_vector)
    label = feature_map[best_match_index]
    print("{}: {} ({}%)".format(
        path, label, int(100*feature_vector[best_match_index])))
