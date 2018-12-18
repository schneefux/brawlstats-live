# -*- encoding:utf8 -*-
#!/usr/bin/env python3
# based on https://gist.github.com/kscottz/242176c5bdb282b0a327

import os
import cv2
import time
import glob

class Template(object):
    def __init__(self, path, scaling_factor):
        self.label = os.path.basename(os.path.splitext(path)[0])
        image = self.source_image = cv2.imread(path)
        image = cv2.resize(image, None,
                           fx=scaling_factor, fy=scaling_factor)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        self.threshold, self.mask = cv2.threshold(
            image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)


class Classifier(object):
    # scale 16:9 (Twitch de facto standard) to
    # * 16:9 phone (runickk)
    # * 21:9 phone (landi)
    # * 3:4 phone (backstabx)
    all_scaling_factors = [1.0, 1.24, 1.35]
    min_match_confidence = 0.70

    def __init__(self, stream_resolution):
        self.stream_resolution = stream_resolution
        self.scale_factor = None
        self.templates = []

    def load_templates(self, template_glob, template_resolution):
        for path in glob.glob(template_glob):
            factor = float(self.stream_resolution) / template_resolution
            self.templates.append(Template(path, factor))

    def classify_image(self, frame):
        '''
        Given a frame, return the name of the first matching template
        or None.
        '''
        # https://www.docs.opencv.org/trunk/d4/dc6/tutorial_py_template_matching.html
        benchmark = time.time()

        need_perfect_factor = self.scale_factor is None
        matching_template = None
        if not need_perfect_factor:
            factors = [self.scale_factor]
        else:
            # try a range of factors until a template matches
            factors = self.all_scaling_factors
            perfect_factor = 1.0
            perfect_factor_confidence = 0.0

        # prerender resized images
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        for factor in factors:
            scaled_frame = cv2.resize(gray_frame, None,
                                      fx=factor, fy=factor)

            for template in self.templates:
                if template.mask.shape[0] > scaled_frame.shape[0] or \
                        template.mask.shape[1] > scaled_frame.shape[1]:
                    continue

                black_frame = cv2.threshold(
                    scaled_frame,
                    template.threshold,
                    255,
                    cv2.THRESH_BINARY)[1]
                matches = cv2.matchTemplate(black_frame,
                                            template.mask,
                                            cv2.TM_CCOEFF_NORMED)
                confidence = matches.max()
                if confidence >= self.min_match_confidence:
                    if need_perfect_factor:
                        if confidence > perfect_factor_confidence:
                            matching_template = template
                            perfect_factor = factor
                            perfect_factor_confidence = confidence
                    else:
                        # early break
                        print("matched template in {}s with confidence {}"
                              .format(time.time() - benchmark,
                                      confidence))
                        return template.label

        if need_perfect_factor and matching_template is not None:
            self.scale_factor = perfect_factor
            print("found perfect factor {} with confidence {}"
                  .format(perfect_factor, perfect_factor_confidence))
            return matching_template.label

        print("matched no templates in {}s"
              .format(time.time() - benchmark))
        return None
