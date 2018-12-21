import logging
from attr import evolve
from queue import Queue, Empty
from threading import Thread

from pipe.sink import Sink

class AsyncPipeline(Sink):
    """
    Defer execution of pipes to a seperate thread
    and queue the result.
    """
    queue_size = 10

    def __init__(self, pipes):
        self.pipes = pipes
        self._state = None
        self._queue = Queue(self.queue_size)
        self._changes = Queue(self.queue_size)

    def start(self):
        for pipe in self.pipes:
            pipe.start()

        self._thread = Thread(
            target=self._process_async_forever, args=())
        self._thread.daemon = True
        self._thread.start()

    def process(self, frame, state):
        self._state = state
        if self._queue.full():
            logging.warning(
                "async pipeline queue is full, dropping frame")
        else:
            self._queue.put(frame)
        return {}

    def get_change(self):
        try:
            return self._changes.get_nowait()
        except Empty:
            return {}

    def _process_async_forever(self):
        while True:
            frame = self._queue.get()
            changes = {}
            for pipe in self.pipes:
                changes = {
                    **changes,
                    **pipe.process(frame,
                                   evolve(self._state, **changes))
                }
            self._changes.put(changes)
