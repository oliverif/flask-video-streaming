import os
import cv2
from base_camera import BaseCamera
import time
from webcamstream import WebcamVideoStream
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
        camera = WebcamVideoStream(src=Camera.video_source).start()
        prev_time = time.time()
        prev_img = camera.read_img()
        while True:
            # read current frame
            img = camera.read_img()
            t = time.time()
            if t - prev_time > 5:
                prev_time = t
                print(prev_img == img)
                print(type(img))
                prev_img = img

            yield img, t
