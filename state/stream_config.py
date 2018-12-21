from attr import attrs, attrib

@attrs(frozen=True)
class StreamConfig(object):
    resolution = attrib(type=int)
    # stream * ratio factor = 16:9
    aspect_ratio_factor = attrib(type=float, default=None)
