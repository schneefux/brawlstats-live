from attr import attrs, attrib

@attrs(frozen=True)
class StreamConfig(object):
    resolution = attrib(type=int)
    url = attrib(type=str, default=None)
    screen_box = attrib(default=None)
    freeze_screen_box = attrib(default=False)
    template_positions = attrib(default=dict())
