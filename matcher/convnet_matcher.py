import cv2
import numpy as np
from keras.models import load_model
from keras.backend import image_data_format

from matcher.matcher import Matcher

class ConvnetMatcher(Matcher):
    min_confidence = 0.90

    def __init__(self, image_shape, feature_map):
        self._image_shape = image_shape
        self._feature_map = feature_map

    def load_model(self, path):
        self._model = load_model(path)

    def classify(self, frame, stream_config):
        screen_box = stream_config.screen_box
        # .shape and array index: y, x
        # screen box is absolute to the stream
        frame = frame[screen_box[0][1]:screen_box[1][1],
                      screen_box[0][0]:screen_box[1][0]]
    
        frame = cv2.resize(frame, self._image_shape)

        if image_data_format() == "channels_first":
            # cv2 is channel last, keras+theano is channels first
            frame = np.moveaxis(frame, -1, 0)

        # cv2 bgr to keras rgb
        frame = frame[...,::-1]
        # cv2 int to keras float
        frame = frame.astype(np.float32)
        # rescale
        frame = frame / 255.0
        # add feature vector placeholder
        frame = frame.reshape((1, ) + frame.shape)

        feature_vector = self._model.predict(frame)[0]

        return [(self._feature_map[i], feature_vector[i])
                for i in range(len(feature_vector))
                if feature_vector[i] > self.min_confidence]
