import time
from threading import Timer
from classifier import Classifier

class StreamWatcher(object):
    def start(self, stream, fps, config):
        self._stream = stream
        self._fps = fps
        self._classifiers = self._create_classifiers(config)
        self._running = True
        self._tick()

    def stop(self):
        self._running = False
        self._timer.cancel()

    def _create_classifiers(self, config):
        classifier = dict()
        classifier["screen"] = Classifier(
            config.stream_resolution)
        classifier["post_match"] = Classifier(
            config.stream_resolution)
        classifier["screen"].load_templates(
            "templates/screen/*.png",
            config.template_resolution)
        classifier["post_match"].load_templates(
            "templates/post_match/*.png",
            config.template_resolution)
        return classifier

    def _tick(self):
        if not self._running:
            return

        start_time = time.time()
        self._watch_frame(self._classifiers, self._stream)

        seconds_until_next = max(
            1.0/self._fps - (time.time() - start_time), 0)
        self._timer = Timer(seconds_until_next, self._tick)
        self._timer.start()

    def _watch_frame(self, classifier, stream):
        frame = stream.get_frame()

        screen = classifier["screen"].classify(frame)
        if screen is not None:
            classifier["post_match"].scale_factor = \
                classifier["screen"].scale_factor
            match_result = classifier["post_match"].classify(frame)
            if match_result is None:
                # misclassified
                classifier["post_match"].scale_factor = \
                    classifier["screen"].scale_factor = None
                # save screenshot
                filename = "{}_{}.png".format(
                    stream.channel, int(time.time()))
                cv2.imwrite(filename, frame)

            print("current frame shows screen {} with {}!"
                  .format(screen, match_result))

