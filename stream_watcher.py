import cv2
import time
from attr import evolve
from state.game_state import GameState, Screen
from threading import Timer
from classifiers.template_matcher import TemplateMatcher

class StreamWatcher(object):
    def start(self, stream, config, stream_config):
        self.state = GameState(stream_config=stream_config,
                               screen=None)
        self._stream = stream
        self._fps = config.max_fps
        self._matchers = self._create_matchers(config)
        self._running = True
        self._tick()

    def stop(self):
        self._running = False
        self._timer.cancel()

    @staticmethod
    def _create_matchers(config):
        matchers = dict()
        matchers["screen"] = TemplateMatcher()
        matchers["post_match"] = TemplateMatcher()
        matchers["screen"].load_templates(
            "templates/screen/*.png",
            config.template_resolution, True)
        matchers["post_match"].load_templates(
            "templates/post_match/*.png",
            config.template_resolution, True)
        return matchers

    def _tick(self):
        if not self._running:
            return

        start_time = time.time()
        self.state = self._watch_frame(self._stream,
                                       self._matchers,
                                       self.state)

        seconds_until_next = max(
            1.0/self._fps - (time.time() - start_time), 0)
        self._timer = Timer(seconds_until_next, self._tick)
        self._timer.start()

    @staticmethod
    def _watch_frame(stream, matchers, state):
        frame = stream.get_frame()

        screen_label, stream_config = matchers["screen"].classify(
            frame, state.stream_config)
        if screen_label is not None:
            result_label, stream_config = matchers["post_match"]\
                .classify(frame, state.stream_config)
            if result_label is not None:
                state = evolve(state, screen=Screen(screen_label))
            else:
                # misclassified
                stream_config = evolve(stream_config,
                                       aspect_ratio_factor=None)
                # save screenshot
                filename = "{}_{}.png".format(
                    stream.channel, int(time.time()))
                cv2.imwrite(filename, frame)

            print("current frame shows screen {} with {}!"
                  .format(screen_label, result_label))

        return evolve(state, stream_config=stream_config)
