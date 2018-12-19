# -*- encoding:utf8 -*-
#!/usr/bin/env python3
# based on https://gist.github.com/kscottz/242176c5bdb282b0a327

import os
import cv2
import time
import glob
import json

class Template(object):
    def __init__(self, path, label, scaling_factor):
        self.label = label
        image = self.source_image = cv2.imread(path)
        image = cv2.resize(image, None,
                           fx=scaling_factor, fy=scaling_factor)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        self.threshold, self.mask = cv2.threshold(
            image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        self.position = None
        self.shape = self.mask.shape


class Classifier(object):
    # scale 16:9 (Twitch de facto standard) to
    # * 16:9 phone (runickk)
    # * 21:9 phone (landi)
    # * 3:4 phone (backstabx)
    all_scaling_factors = [1.0, 1.24, 1.35]
    min_match_confidence = 0.70

    def __init__(self, stream_resolution):
        self.stream_resolution = stream_resolution
        self.templates = []
        self.scale_factor = None

    def load_templates(self, template_glob, template_resolution):
        paths = glob.glob(template_glob)
        if len(paths) == 0:
            print("template glob yields no paths!")

        for path in paths:
            factor = float(self.stream_resolution) / template_resolution
            name = os.path.basename(os.path.splitext(path)[0])
            self.templates.append(
                Template(path, name, factor))

    def classify(self, frame):
        '''
        Given a frame, return the name of the first matching template
        or None.
        '''
        # https://www.docs.opencv.org/trunk/d4/dc6/tutorial_py_template_matching.html
        benchmark = time.time()

        need_perfect_factor = self.scale_factor is None
        matching_template = None
        if not need_perfect_factor:
            factors = [self.scale_factor]
        else:
            # try a range of factors until a template matches
            factors = self.all_scaling_factors
            perfect_factor = None
            perfect_position = None
            perfect_factor_confidence = 0.0

        # prerender resized images
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        for factor in factors:
            scaled_frame = cv2.resize(gray_frame, None,
                                      fx=factor, fy=factor)

            for template in self.templates:
                position = template.position
                if position is not None:
                    box = template.shape
                    scaled_frame = scaled_frame[
                        position[1]:position[1] + box[0],
                        position[0]:position[0] + box[1]
                    ]

                if template.mask.shape[0] > scaled_frame.shape[0] or \
                        template.mask.shape[1] > scaled_frame.shape[1]:
                    continue

                black_frame = cv2.threshold(
                    scaled_frame,
                    template.threshold,
                    255,
                    cv2.THRESH_BINARY)[1]
                matches = cv2.matchTemplate(black_frame,
                                            template.mask,
                                            cv2.TM_CCOEFF_NORMED)
                _, confidence, _, position = cv2.minMaxLoc(matches)
                if confidence >= self.min_match_confidence:
                    if need_perfect_factor:
                        if confidence > perfect_factor_confidence:
                            matching_template = template
                            perfect_factor = factor
                            perfect_position = position
                            perfect_factor_confidence = confidence
                    else:
                        # early break
                        print("matched template in {}s with confidence {}"
                              .format(time.time() - benchmark,
                                      confidence))
                        return template.label

        if need_perfect_factor and matching_template is not None:
            self.scale_factor = perfect_factor
            matching_template.position = perfect_position
            print("found perfect factor {} with confidence {} at position {}"
                  .format(perfect_factor, perfect_factor_confidence, position))
            return matching_template.label

        return None
