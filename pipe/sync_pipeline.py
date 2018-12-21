from pipe.pipe import Pipe

class SyncPipeline(Pipe):
    """
    Execute pipes serially.
    """
    def __init__(self, pipes):
        self.pipes = pipes

    def start(self):
        for pipe in self.pipes:
            pipe.start()

    def process(self, frame, state):
        for pipe in self.pipes:
            state = pipe.process(frame, state)
        return state
