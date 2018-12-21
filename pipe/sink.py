from pipe.pipe import Pipe

class Sink(Pipe):
    """
    Abstract processing step that does not return a state.
    """
    realtime = True
