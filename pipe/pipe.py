class Pipe(object):
    """
    Abstract processing step that returns a modified state.
    """
    def start(self):
        """
        Set up the pipe.
        """
        raise NotImplementedError()

    def process(self, frame, state):
        """
        Process the frame and return a mutation to the GameState.
        """
        raise NotImplementedError()
