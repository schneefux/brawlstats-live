class StreamSource(object):
    """
    Abstract stream source.
    """
    def get_frame(self):
        raise NotImplementedError()

