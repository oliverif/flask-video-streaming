import time


from threading import Thread
import cv2


class FrameGetter:
    """
    Class that continuously gets frames from a VideoCapture object
    with a dedicated thread.
    """

    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False

    def start(self):
        Thread(target=self.get, args=()).start()
        return self

    def get(self):
        while not self.stopped:
            if not self.grabbed:
                self.stop()
            else:
                (self.grabbed, self.frame) = self.stream.read()

    def stop(self):
        self.stopped = True


class FrameSender:
    """
    Class that continuously sends a frame using a dedicated thread.
    """

    def __init__(self, frame=None):
        self.frame = frame
        self.stopped = False
        self.img = None

    def start(self):
        Thread(target=self.show, args=()).start()
        return self

    def show(self):
        while not self.stopped:
            self.img = cv2.imencode(".jpg", self.frame)[1].tobytes()
            if cv2.waitKey(1) == ord("q"):
                self.stopped = True

    def stop(self):
        self.stopped = True


class Camera:
    frame = None
    img = None

    def __init__(self, delay):
        self.delay = delay
        self.source = 0

    def get_frame(self):
        return self.frame

    def frames(self):
        frame_getter = FrameGetter(self.source).start()
        # frame_sender = FrameSender(frame_getter.frame).start()
        # while frame_sender.img is None:
        #    pass
        # self.img = frame_sender.img

        while True:
            if frame_getter.stopped:  # or frame_sender.stopped:
                # frame_sender.stop()
                frame_getter.stop()
                break

            # frame_sender.frame = frame_getter.frame
            # self.img = frame_sender.img
            self.frame = cv2.imencode(".jpg", frame_getter.frame)[1].tobytes()
