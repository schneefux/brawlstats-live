class Pipe(object):
    """
    Abstract processing step that returns a state modification.
    """
    def start(self):
        """
        Set up the pipe.
        """
        pass

    def process(self, frame, state):
        """
        Process the frame and return a mutation to the GameState.
        """
        raise NotImplementedError()
