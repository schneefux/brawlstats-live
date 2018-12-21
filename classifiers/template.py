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
    is_position_fixed = attrib()
    resolution = attrib()


@attrs
class Template(object):
    """
    Store a template.
    """
    template_image = attrib()
    image = attrib()
    position = attrib()
    shape = attrib()

    @classmethod
    def from_template_image(cls, template_image, target_resolution):
        image = cls._resized_image(template_image, target_resolution)
        return cls(template_image=template_image,
            position=None,
            image=image,
            shape=image.shape)

    @staticmethod
    def _resized_image(template_image, target_resolution):
        aspect_ratio_factor = float(target_resolution) \
            / template_image.resolution
        image = cv2.resize(template_image.image, None,
                           fx=aspect_ratio_factor,
                           fy=aspect_ratio_factor,
                           interpolation=cv2.INTER_AREA)
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def load_template_images(path_glob, resolution, is_position_fixed):
    template_images = []
    paths = glob.glob(path_glob)
    if len(paths) == 0:
        logging.warning("template glob %s yields no paths!",
                        path_glob)

    for path in paths:
        name = os.path.basename(os.path.splitext(path)[0])
        template_images.append(
            TemplateImage(image=cv2.imread(path),
                          label=name,
                          resolution=resolution,
                          is_position_fixed=is_position_fixed))

    return template_images
