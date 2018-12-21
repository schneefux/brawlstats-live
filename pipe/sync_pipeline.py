from attr import evolve

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
        changes = {}
        for pipe in self.pipes:
            changes = {
                **changes,
                **pipe.process(frame, evolve(state, **changes))
            }
        return changes
