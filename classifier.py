# -*- encoding:utf8 -*-
#!/usr/bin/env python3
# based on https://gist.github.com/kscottz/242176c5bdb282b0a327

import os
import numpy as np
import cv2
import time
import glob

# streamers scale their streams a bit
ALL_SCALING_FACTORS = np.linspace(0.90, 1.30, 10)
MIN_MATCH_CONFIDENCE = 0.80

# load templates
# all should be taken from the exact same scale!
templates = dict()
template_threshold = dict()
for path in glob.glob("templates/*.png"):
    template = cv2.imread(path)
    # 480p stream / 1080p phone
    resolution_factor = 480.0 / 1080.0
    template = cv2.resize(template, None,
                          fx=resolution_factor, fy=resolution_factor)
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    threshold, template = cv2.threshold(template, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    name = os.path.basename(os.path.splitext(path)[0])
    templates[name] = template
    template_threshold[name] = threshold

print("loaded templates {}".format(templates.keys()))

# assumes that the streamer's scaling never changes
# and that the same factor works for all
# if it works for one (which might not be true…)
scale_factor_cache = dict()

def classify_image(frame, cache_key=""):
    '''
    Given a frame, return the name of the first matching template
    or None.
    '''
    # https://www.docs.opencv.org/trunk/d4/dc6/tutorial_py_template_matching.html
    BENCH = time.time()

    found_perfect_factor = cache_key in scale_factor_cache
    need_perfect_factor = not found_perfect_factor
    if found_perfect_factor:
        factors = [scale_factor_cache[cache_key]]
    else:
        # try a range of factors until a template matches
        factors = ALL_SCALING_FACTORS
        perfect_factor = 1.0
        perfect_factor_confidence = 0.0
        perfect_factor_template_name = ""

    # prerender resized images 
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    for factor in factors:
	scaled_frame = cv2.resize(gray_frame, None,
                                  fx=factor, fy=factor)

        # try all templates
        for template_name, template in templates.items():
            if template.shape[0] > scaled_frame.shape[0] or \
                    template.shape[1] > scaled_frame.shape[1]:
                # too large anyways
                continue

            black_frame = cv2.threshold(
                scaled_frame,
                template_threshold[template_name],
                255,
                cv2.THRESH_BINARY)[1]
            matches = cv2.matchTemplate(black_frame,
                                        template, cv2.TM_CCOEFF_NORMED)
            confidence = matches.max()
            if confidence >= MIN_MATCH_CONFIDENCE:
                if need_perfect_factor:
                    if confidence > perfect_factor_confidence:
                        found_perfect_factor = True
                        perfect_factor = factor
                        perfect_factor_confidence = confidence
                        perfect_factor_template_name = template_name
                else:
                    # early break
                    print("matched template in {}s with confidence {}"
                          .format(time.time() - BENCH, confidence))
                    return template_name

    if need_perfect_factor and found_perfect_factor:
        scale_factor_cache[cache_key] = perfect_factor
        print("found perfect factor {} with confidence {}"
              .format(perfect_factor, perfect_factor_confidence))
        return perfect_factor_template_name

    print("matched no templates in {}s".format(time.time() - BENCH))
    return None
