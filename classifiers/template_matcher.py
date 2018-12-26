# -*- encoding:utf8 -*-
#!/usr/bin/env python3

import os
import cv2
import glob
import json
import time
import numpy as np
from math import sqrt

from classifiers.template import Template, TemplateImage

class TemplateMatcher(object):
    """
    Compare template images to a frame and return the matches.
    """
    min_match_confidence = 0.70
    # minimum distance two matches need to have
    offset_tolerance = 15

    def load_templates(self, path_glob, resolution):
        self.template_images = []
        paths = glob.glob(path_glob)
        if len(paths) == 0:
            logging.warning("template glob %s yields no paths!",
                            path_glob)

        for path in paths:
            path_no_ext = os.path.splitext(path)[0]
            name = os.path.basename(path_no_ext)
            json_path = path_no_ext + ".json"
            bounding_box = None

            if os.path.isfile(json_path):
                with open(json_path, "r") as json_file:
                    box = json.load(json_file)
                    bounding_box = ((box["x1"], box["y1"]),
                                    (box["x2"], box["y2"]))

            self.template_images.append(
                TemplateImage(image=cv2.imread(path),
                              label=name,
                              resolution=resolution,
                              bounding_box=bounding_box))

    def classify(self, frame, stream_config,
                 break_after_first_match=False):
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
                target_resolution=gray_frame.shape[0])

            template_position = stream_config.template_positions.get(
                template.template_image.label)

            query_frame = gray_frame

            if template_position is not None:
                # cut out box where template is expected
                h, w = template.image.shape
                x = max(template_position[0] - screen_box[0][0], 0)
                y = max(template_position[1] - screen_box[0][1], 0)
                query_frame = gray_frame[y:y+h, x:x+w]
            else:
                template_position = (0, 0)

                box = template.bounding_box
                if box is not None:
                    x1 = int(box[0][0] * gray_frame.shape[1])
                    y1 = int(box[0][1] * gray_frame.shape[0])
                    x2 = int(box[1][0] * gray_frame.shape[1])
                    y2 = int(box[1][1] * gray_frame.shape[0])
                    query_frame = gray_frame[y1:y2, x1:x2]

            if template.image.shape[0] > query_frame.shape[0] or \
                    template.image.shape[1] > query_frame.shape[1]:
                continue

            correlation_map = cv2.matchTemplate(
                query_frame, template.image, cv2.TM_CCOEFF_NORMED)
            positions = np.where(
                correlation_map > self.min_match_confidence)

            for position in zip(*positions):
                # translate position back to original frame
                position_t = (position[0] + screen_box[0][0]
                              + template_position[0],
                              position[1] + screen_box[0][1]
                              + template_position[1])

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
                    if break_after_first_match:
                        break

        return matches
