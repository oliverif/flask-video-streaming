import time


from threading import Thread
import cv2


class FrameSender:
    """
    Class that continuously sends a frame using a dedicated thread.
    """

    def __init__(self, frame=None):
        self.frame = frame
        self.stopped = False

    def start(self):
        Thread(target=self.show, args=()).start()
        return self

    def show(self):
        while not self.stopped:
            cv2.imshow("Video", self.frame)
            if cv2.waitKey(1) == ord("q"):
                self.stopped = True

    def stop(self):
        self.stopped = True


class Camera:
    """An emulated camera implementation that streams a repeated sequence of
    files 1.jpg, 2.jpg and 3.jpg at a rate of one frame per second."""

    imgs = [open(f + ".jpg", "rb").read() for f in ["1", "2", "3"]]

    @staticmethod
    def frames():
        frame_getter = FrameGetter(source).start()
        frame_sender = FrameSender(frame_getter.frame).start()
        cps = CountsPerSec().start()

        while True:
            if video_getter.stopped or video_shower.stopped:
                video_shower.stop()
                video_getter.stop()
                break

            frame = video_getter.frame
            frame = putIterationsPerSec(frame, cps.countsPerSec())
            video_shower.frame = frame
            cps.increment()
