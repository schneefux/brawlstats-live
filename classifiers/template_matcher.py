# -*- encoding:utf8 -*-
#!/usr/bin/env python3

import os
import cv2
import glob
import json
import time
import logging
import numpy as np
from math import sqrt

from classifiers.template import Template, TemplateImage

class TemplateMatcher(object):
    """
    Compare template images to a frame and return the matches.
    """
    min_match_confidence = 0.75
    # minimum px distance between two matches
    offset_tolerance = 15

    def load_templates(self, path_glob,
                       screen_width, screen_height):
        self.template_images = []
        paths = glob.glob(path_glob)
        if len(paths) == 0:
            logging.warning("template glob %s yields no paths!",
                            path_glob)

        for path in paths:
            path_no_ext = os.path.splitext(path)[0]
            name = os.path.basename(path_no_ext)

            bounding_box = ((0, 0), (1.0, 1.0))
            for json_path in ("default.json", path_no_ext + ".json"):
                if os.path.isfile(json_path):
                    with open(json_path, "r") as json_file:
                        box = json.load(json_file)
                        bounding_box = ((box["x1"], box["y1"]),
                                        (box["x2"], box["y2"]))

            self.template_images.append(
                TemplateImage(image=cv2.imread(path),
                              label=name,
                              screen_width=screen_width,
                              screen_height=screen_height,
                              bounding_box=bounding_box))

    def classify(self, frame, stream_config,
                 only_first_match=False):
        """
        Given a frame, return a list of name, position tuples
        of matching templates.
        """
        screen_box = stream_config.screen_box
        # .shape and array index: y, x
        # screen box is absolute to the stream
        frame = frame[screen_box[0][1]:screen_box[1][1],
                      screen_box[0][0]:screen_box[1][0]]

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        matches = []

        for template_image in self.template_images:
            template = Template.from_template_image(
                template_image=template_image,
                target_height=gray_frame.shape[0],
                target_width=gray_frame.shape[1])

            template_position = stream_config.template_positions.get(
                template.template_image.label)

            if template_position is not None:
                # cut out box where template is expected
                h, w = template.image.shape
                # template_position is absolute to the stream
                x = template_position[0] - screen_box[0][0]
                y = template_position[1] - screen_box[0][1]
                if not (0 <= x < gray_frame.shape[1] - w \
                        and 0 <= y < gray_frame.shape[0] - h):
                    continue
                query_frame = gray_frame[y:y+h, x:x+w]
            else:
                # bounding box is relative to the screen box
                box = template.bounding_box
                x1 = int(box[0][0] * gray_frame.shape[1])
                y1 = int(box[0][1] * gray_frame.shape[0])
                x2 = int(box[1][0] * gray_frame.shape[1])
                y2 = int(box[1][1] * gray_frame.shape[0])
                query_frame = gray_frame[y1:y2, x1:x2]
                template_position = (
                    x1 + screen_box[0][0],
                    y1 + screen_box[0][1])

            if template.image.shape[0] > query_frame.shape[0] or \
                    template.image.shape[1] > query_frame.shape[1]:
                continue

            correlation_map = cv2.matchTemplate(
                query_frame, template.image, cv2.TM_CCOEFF_NORMED)
            # positions: [y, x]
            positions = np.where(
                correlation_map > self.min_match_confidence)

            for position_y, position_x in zip(*positions):
                # position_t is absolute to the screen
                position_t = (position_x + template_position[0],
                              position_y + template_position[1])

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
                    if only_first_match:
                        return matches

        return matches
