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
    resolution = attrib()


@attrs
class Template(object):
    """
    Store a template.
    """
    template_image = attrib()
    image = attrib()

    @classmethod
    def from_template_image(cls, template_image, target_resolution):
        image = cls._resized_image(template_image, target_resolution)
        return cls(template_image=template_image, image=image)

    @staticmethod
    def _resized_image(template_image, target_resolution):
        factor = float(target_resolution) / float(template_image.resolution)
        image = cv2.resize(template_image.image, None,
                           fx=factor, fy=factor,
                           interpolation=cv2.INTER_AREA)
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


