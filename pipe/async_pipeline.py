import logging
from queue import Queue
from threading import Thread

from pipe.sink import Sink

class AsyncPipeline(Sink):
    """
    Defer execution of pipes to a seperate thread.
    """
    queue_size = 10

    def __init__(self, pipes):
        self.pipes = pipes
        self._queue = Queue(self.queue_size)

    def start(self):
        for pipe in self.pipes:
            pipe.start()

        self._thread = Thread(
            target=self._process_async_forever, args=())
        self._thread.daemon = True
        self._thread.start()

    def process(self, frame, state):
        if self._queue.full():
            logging.warning(
                "async pipeline queue is full, dropping frame")
        else:
            self._queue.put((frame, state))
        return state

    def _process_async_forever(self):
        while True:
            frame, state = self._queue.get()
            for pipe in self.pipes:
                state = pipe.process(frame, state)
