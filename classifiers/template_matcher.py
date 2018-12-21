# -*- encoding:utf8 -*-
#!/usr/bin/env python3

import os
import cv2
import glob
from attr import attrs, attrib, evolve

@attrs(frozen=True)
class TemplateImage(object):
    """
    Store meta data and cache an image from the file system.
    """
    image = attrib()
    label = attrib()
    is_position_fixed = attrib()
    resolution = attrib()

@attrs
class Template(object):
    template_image = attrib()
    position = attrib()
    image = attrib()
    threshold = attrib()
    mask = attrib()
    shape = attrib()

    @classmethod
    def from_template_image(cls, template_image, stream_resolution):
        image = cls._resized_image(template_image, stream_resolution)
        threshold, mask = cv2.threshold(
            image,
            0, 255,
            cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        return cls(template_image=template_image,
            position=None,
            image=image,
            threshold=threshold,
            mask=mask,
            shape=mask.shape)

    @staticmethod
    def _resized_image(template_image, stream_resolution):
        aspect_ratio_factor = float(stream_resolution) \
            / template_image.resolution
        image = cv2.resize(template_image.image, None,
                           fx=aspect_ratio_factor,
                           fy=aspect_ratio_factor)
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


class TemplateMatcher(object):
    # scale 16:9 (Twitch de facto standard) to
    # * 16:9 phone (runickk)
    # * 21:9 phone (landi)
    # * 3:4 phone (backstabx)
    # * 21:9 phone with streamer borders (daenerysgaming)
    common_aspect_ratio_factors = [1.0, 1.24, 1.36, 1.44]
    min_match_confidence = 0.70

    def __init__(self):
        self.template_images = []

    def load_templates(self, path_glob, resolution,
                       is_position_fixed):
        paths = glob.glob(path_glob)
        if len(paths) == 0:
            print("template glob yields no paths!")

        for path in paths:
            name = os.path.basename(os.path.splitext(path)[0])
            self.template_images.append(
                TemplateImage(image=cv2.imread(path),
                              label=name,
                              resolution=resolution,
                              is_position_fixed=is_position_fixed))

    def classify(self, frame, stream_config):
        '''
        Given a frame, return the name of the first matching template
        or None.
        '''
        templates = []
        for template_image in self.template_images:
            templates.append(Template.from_template_image(
                template_image=template_image,
                stream_resolution=stream_config.resolution))

        search_aspect_ratio = stream_config.aspect_ratio_factor is None
        matching_template = None
        matching_template_position = None
        if search_aspect_ratio:
            aspect_ratio_factors = self.common_aspect_ratio_factors
            aspect_ratio_factor = None
            aspect_ratio_confidence = 0.0
        else:
            aspect_ratio_factors = [stream_config.aspect_ratio_factor]

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        for factor in aspect_ratio_factors:
            scaled_frame = cv2.resize(gray_frame, None,
                                      fx=factor, fy=factor)

            for template in templates:
                if template.template_image.is_position_fixed and \
                        template.position is not None:
                    # cut out box where template is expected
                    box = template.shape
                    scaled_frame = scaled_frame[
                        template.position[1]:template.position[1]
                            + box[0],
                        template.position[0]:template.position[0]
                            + box[1]
                    ]

                if template.mask.shape[0] > scaled_frame.shape[0] or \
                        template.mask.shape[1] > scaled_frame.shape[1]:
                    continue

                black_frame = cv2.threshold(
                    scaled_frame,
                    template.threshold, 255,
                    cv2.THRESH_BINARY)[1]
                matches = cv2.matchTemplate(black_frame,
                                            template.mask,
                                            cv2.TM_CCOEFF_NORMED)
                _, confidence, _, position = cv2.minMaxLoc(matches)
                if confidence >= self.min_match_confidence:
                    if search_aspect_ratio:
                        if confidence > aspect_ratio_confidence:
                            matching_template = template
                            matching_template_position = position
                            aspect_ratio_factor = factor
                            aspect_ratio_confidence = confidence
                    else:
                        # early break
                        return template.template_image.label, stream_config

        if search_aspect_ratio and matching_template is not None:
            stream_config = evolve(stream_config,
                aspect_ratio_factor=aspect_ratio_factor)
            matching_template.position = matching_template_position
            return matching_template.template_image.label, stream_config

        return None, stream_config
