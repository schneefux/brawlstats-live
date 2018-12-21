class Pipe(object):
    """
    Abstract processing step that returns a modified state.
    """
    realtime = False

    def start(self):
        raise NotImplementedError()

    def process(self, frame, state):
        raise NotImplementedError()
