from attr import attrs, attrib

@attrs(frozen=True)
class StreamConfig(object):
    resolution = attrib(type=int)
    max_fps = attrib(type=float)
    url = attrib(type=str, default=None)
    screen_box = attrib(default=None)
    template_positions = attrib(default=dict())
