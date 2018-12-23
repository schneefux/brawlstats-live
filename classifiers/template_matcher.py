# -*- encoding:utf8 -*-
#!/usr/bin/env python3

import os
import cv2
import glob
import time
from attr import evolve

from classifiers.template import Template, TemplateImage, \
    load_template_images

class TemplateMatcher(object):
    """
    Compare template images to a frame.
    Convert the frame to grayscale and resize.
    """
    min_match_confidence = 0.70

    def load_templates(self, path_glob, resolution):
        self.template_images = load_template_images(
            path_glob, resolution)

    def classify(self, frame, stream_config):
        """
        Given a frame, return the name of the first matching template
        or None.
        """
        screen_box = stream_config.screen_box
        frame = frame[screen_box[0][1]:screen_box[1][1],
                      screen_box[0][0]:screen_box[1][0]]

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        for template_image in self.template_images:
            template = Template.from_template_image(
                template_image=template_image,
                target_height=gray_frame.shape[0])

            if template.image.shape[0] > gray_frame.shape[0] or \
                    template.image.shape[1] > gray_frame.shape[1]:
                continue

            template_position = stream_config.template_positions.get(
                template.template_image.label)

            if template_position is not None:
                # cut out box where template is expected
                h, w = template.image.shape
                x = template_position[0] - screen_box[0][0]
                y = template_position[1] - screen_box[0][1]
                gray_frame = gray_frame[y:y+h, x:x+w]

            matches = cv2.matchTemplate(gray_frame,
                                        template.image,
                                        cv2.TM_CCOEFF_NORMED)
            _, confidence, _, position = cv2.minMaxLoc(matches)
            if confidence >= self.min_match_confidence:
                template_position = (position[0] + screen_box[0][0],
                                     position[1] + screen_box[0][1])
                # early break
                return template.template_image.label, template_position

        return None, None
