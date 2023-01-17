import os
import cv2
from base_camera import BaseCamera
import time
from imutils.video import VideoStream
from threading import Thread


class Camera(BaseCamera):
    video_source = 0
    fps = 60

    def __init__(self, delay):
        if os.environ.get("VIDEOSTREAM_CAMERA_SOURCE"):
            Camera.set_video_source(int(os.environ["VIDEOSTREAM_CAMERA_SOURCE"]))
        super(Camera, self).__init__(delay)

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def frames():
        camera = VideoStream(src=Camera.video_source, framerate=Camera.fps).start()
        while True:
            # read current frame
            img = camera.read()
            t = time.time()
            yield cv2.imencode(".jpg", img)[1].tobytes(), t
