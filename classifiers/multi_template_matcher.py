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
            path_glob, resolution, False)

    def classify(self, frame, stream_config):
        """
        Given a frame, return a list of name, position tuples
        of matching templates.
        """
        templates = []
        for template_image in self.template_images:
            resolution = stream_config.resolution \
                / stream_config.aspect_ratio_factor
            templates.append(Template.from_template_image(
                template_image=template_image,
                target_resolution=resolution))

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        matches = []

        for template in templates:
            if template.shape[0] > gray_frame.shape[0] or \
                    template.shape[1] > gray_frame.shape[1]:
                continue

            res = cv2.matchTemplate(gray_frame,
                                    template.image,
                                    cv2.TM_CCOEFF_NORMED)
            positions = np.where(res > self.min_match_confidence)
            for position in zip(*positions):
                for _, match_position in matches:
                    dist = sqrt((position[0]-match_position[0])**2 + \
                                (position[1]-match_position[1])**2)
                    if dist < self.offset_tolerance:
                        # there is an existing match close to this one
                        break
                else:
                    matches.append((template.template_image.label,
                                    position))

        return matches
