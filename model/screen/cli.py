#!/usr/bin/env python3
import cv2
import sys
import numpy as np
from keras.models import load_model
from keras.backend import image_data_format
from keras.preprocessing.image import img_to_array, load_img

from config import shape, feature_map, channels_first

model = load_model("model.h5")

def load_with_cv2(path):
    frame = cv2.imread(path)
    frame = cv2.resize(frame, shape)
    
    if channels_first:
        # cv2 is channel last, keras+theano is channels first
        frame = np.moveaxis(frame, -1, 0)

    # cv2 bgr to keras rgb
    frame = frame[...,::-1]
    return frame

def load_with_keras(path):
    frame = load_img(path)
    frame = frame.resize(shape)
    frame = img_to_array(frame)
    return frame

for path in sys.argv[1:]:
    frame = load_with_cv2(path)
    frame = frame / 255.0
    frame = frame.reshape((1, ) + frame.shape)

    feature_vector = model.predict(frame)[0]
    matches = [(feature_map[i], feature_vector[i])
               for i in range(len(feature_vector))
               if feature_vector[i] > 0.5]
    for label, confidence in matches:
        print("{}: {} ({}%)".format(path, label, int(100*confidence)))
    if len(matches) == 0:
        print("{}: no match".format(path))
