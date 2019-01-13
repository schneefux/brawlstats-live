import queue
import logging
from attr import evolve
from threading import Thread

from pipe.sink import Sink

class AsyncPipeline(Sink):
    """
    Defer execution of child pipes to a seperate thread
    and store the state mutation transaction.
    """
    queue_size = 10

    def __init__(self, pipes):
        self.running = False
        self.pipes = pipes
        self._state = None
        self._queue = queue.Queue(self.queue_size)
        self._changes = dict()

    def start(self):
        for pipe in self.pipes:
            pipe.start()

        self.running = True
        self._thread = Thread(target=self._process_async_forever)
        self._thread.daemon = True
        self._thread.start()

    def stop(self):
        self.running = False

    def process(self, frame, state):
        try:
            self._queue.put_nowait((frame, state))
        except queue.Full:
            logging.warning(
                "async pipeline queue is full, dropping frame")
        return {}

    @property
    def processing(self):
        return not self._queue.empty()

    def reset_changes(self):
        changes = self._changes
        self._changes = dict()
        return changes

    def _process_async_forever(self):
        while self.running:
            frame, state = self._queue.get()
            for pipe in self.pipes:
                transaction_state = evolve(state, **self._changes)
                self._changes = {
                    **self._changes,
                    **pipe.process(frame, transaction_state)
                }
