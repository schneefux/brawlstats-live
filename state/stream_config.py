from attr import attrs, attrib

@attrs(frozen=True)
class StreamConfig(object):
    resolution = attrib(type=int)
    channel = attrib(type=str, default=None)
    screen_box = attrib(default=None)
    template_positions = attrib(default=dict())
