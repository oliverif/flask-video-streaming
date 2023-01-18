# import the necessary packages
from threading import Thread
import cv2


class WebcamVideoStream:
    def __init__(self, src=0, name="WebcamVideoStream"):
        # initialize the video camera stream and read the first frame
        # from the stream
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()

        self.img = cv2.imencode(".jpg", self.frame)[1].tobytes()
        # initialize the thread name
        self.name = name

        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        t = Thread(target=self.update, name=self.name, args=())
        t.daemon = True
        t.start()
        # t2 = Thread(target=self.encode, name="Encoder", args=())
        # t2.daemon = True
        # t2.start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return

            # otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def encode(self):
        while True:
            if self.stopped:
                return
            self.img = cv2.imencode(".jpg", self.frame)[1].tobytes()

    def read(self):
        # return the frame most recently read
        return self.frame

    def read_img(self):
        return self.img

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
