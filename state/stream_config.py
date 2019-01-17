from attr import attrs, attrib

@attrs(frozen=True)
class StreamConfig(object):
    resolution = attrib(type=int)
    max_fps = attrib(type=float)
    url = attrib(type=str, default=None)
    movement_frame = attrib(default=None)
    previous_frame = attrib(default=None)
    screen_box = attrib(default=None)
    screen_box_sensitivity = attrib(type=float, default=0.2)
    template_positions = attrib(default=dict())
