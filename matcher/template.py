import os
import cv2
import glob
import logging
from attr import attrs, attrib

@attrs(frozen=True)
class TemplateImage(object):
    """
    Store an image and its meta data.
    """
    image = attrib()
    label = attrib()
    screen_width = attrib()
    screen_height = attrib()
    bounding_box = attrib()


@attrs
class Template(object):
    """
    Store a template.
    """
    template_image = attrib()
    image = attrib()

    @classmethod
    def from_template_image(cls, template_image,
                            target_width, target_height):
        image = cls._resized_image(template_image,
                                   target_width, target_height)
        return cls(template_image=template_image, image=image)

    @staticmethod
    def _resized_image(template_image,
                       target_width, target_height):
        factor = min(
            target_width / float(template_image.screen_width),
            target_height / float(template_image.screen_height))
        image = cv2.resize(template_image.image, None,
                           fx=factor, fy=factor,
                           interpolation=cv2.INTER_AREA)
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    @property
    def bounding_box(self):
        return self.template_image.bounding_box
