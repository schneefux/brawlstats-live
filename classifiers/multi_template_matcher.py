# -*- encoding:utf8 -*-
#!/usr/bin/env python3

import os
import cv2
import glob
import time
import numpy as np
from math import sqrt

from classifiers.template import Template, TemplateImage, \
    load_template_images

class MultiTemplateMatcher(object):
    """
    Compare template images to a frame.
    Convert the frame to grayscale and resize.
    """
    min_match_confidence = 0.70
    # minimum distance two matches need to have
    offset_tolerance = 15

    def load_templates(self, path_glob, resolution):
        self.template_images = load_template_images(
            path_glob, resolution)

    def classify(self, frame, stream_config):
        """
        Given a frame, return a list of name, position tuples
        of matching templates.
        """
        screen_box = stream_config.screen_box
        frame = frame[screen_box[0][1]:screen_box[1][1],
                      screen_box[0][0]:screen_box[1][0]]

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        matches = []

        for template_image in self.template_images:
            template = Template.from_template_image(
                template_image=template_image,
                target_height=gray_frame.shape[0])

            if template.image.shape[0] > gray_frame.shape[0] or \
                    template.image.shape[1] > gray_frame.shape[1]:
                continue

            res = cv2.matchTemplate(gray_frame,
                                    template.image,
                                    cv2.TM_CCOEFF_NORMED)
            positions = np.where(res > self.min_match_confidence)

            for position in zip(*positions):
                # translate position for full stream coordinates
                position_t = (position[0] + screen_box[0][0],
                              position[1] + screen_box[0][1])

                for _, match_position in matches:
                    dist = sqrt(
                        (position_t[0]-match_position[0])**2 + \
                        (position_t[1]-match_position[1])**2)
                    if dist < self.offset_tolerance:
                        # ignore a close similar match
                        break
                else:
                    matches.append((template.template_image.label,
                                    position_t))

        return matches
