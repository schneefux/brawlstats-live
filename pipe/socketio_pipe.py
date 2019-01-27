import json
import socketio
import eventlet
import eventlet.wsgi
from queue import Queue, Empty
from threading import Thread
from flask import Flask, render_template

from pipe.pipe import Pipe
from state.enum.screen import Screen

class SocketioPipe(Pipe):
    def start(self):
        self._sio = socketio.Server()
        self._app = Flask(__name__,
            template_folder="../web/templates")
        self._app.wsgi_app = socketio.WSGIApp(self._sio,
            self._app.wsgi_app)

        # add routes
        self._app.add_url_rule("/", "index", self._index)

        # messages must be sent from the same thread
        # the server is started from
        self._message_queue = Queue()
        thread = Thread(target=self._run_server)
        thread.daemon = True
        thread.start()
    
    def _send_messages_forever(self):
        while True:
            try:
                self._sio.emit("update", self._message_queue.get_nowait())
            except Empty:
                pass
            eventlet.sleep()

    def _run_server(self):
        eventlet.spawn(self._send_messages_forever)
        eventlet.wsgi.server(eventlet.listen(("", 5000)), self._app)

    def _index(self):
        return render_template("index.html")

    def process(self, frame, state):
        if state.last_change is not None and \
            state.last_queue is not None and \
            state.timestamp - state.last_queue < 300 and \
            state.timestamp - state.last_change > 0.2: # s
            self._message_queue.put({
                "timestamp": state.timestamp,
                "ingame": state.screen == Screen.GEMGRAB_INGAME,
                "screen": state.screen.name if state.screen else None,
                "blue_team": [b.name for b in state.blue_team],
                "blue_gems": state.blue_gems,
                "red_gems": state.red_gems,
                "red_team": [b.name for b in state.red_team],
                "taking_damage": state.taking_damage,
            })

        return {}
