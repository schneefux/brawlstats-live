import queue
import logging
from attr import evolve
from threading import Thread

from pipe.sink import Sink

class AsyncPipeline(Sink):
    """
    Defer execution of child pipes to a seperate thread
    and queue the resulting changes.
    """
    queue_size = 10

    def __init__(self, pipes):
        self.running = False
        self.pipes = pipes
        self._state = None
        self._queue = queue.Queue(self.queue_size)
        self._changes = queue.Queue(self.queue_size)

    def start(self):
        for pipe in self.pipes:
            pipe.start()

        self.running = True
        self._thread = Thread(
            target=self._process_async_forever, args=())
        self._thread.daemon = True
        self._thread.start()

    def stop(self):
        self.running = False

    def process(self, frame, state):
        self._state = state
        try:
            self._queue.put(frame)
        except queue.Full:
            logging.warning(
                "async pipeline queue is full, dropping frame")
        return {}

    def get_change(self):
        try:
            return self._changes.get_nowait()
        except queue.Empty:
            return {}

    def _process_async_forever(self):
        while self.running:
            frame = self._queue.get()
            changes = {}
            for pipe in self.pipes:
                changes = {
                    **changes,
                    **pipe.process(frame,
                                   evolve(self._state, **changes))
                }
            self._changes.put(changes)
