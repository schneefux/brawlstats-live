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
    height = attrib()


@attrs
class Template(object):
    """
    Store a template.
    """
    template_image = attrib()
    image = attrib()

    @classmethod
    def from_template_image(cls, template_image, target_height):
        image = cls._resized_image(template_image, target_height)
        return cls(template_image=template_image, image=image)

    @staticmethod
    def _resized_image(template_image, target_height):
        factor = float(target_height) / float(template_image.height)
        image = cv2.resize(template_image.image, None,
                           fx=factor, fy=factor,
                           interpolation=cv2.INTER_AREA)
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def load_template_images(path_glob, height):
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
                          height=height))

    return template_images
