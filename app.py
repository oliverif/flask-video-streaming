#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response, request, url_for, redirect

# import camera driver
if os.environ.get("CAMERA"):
    Camera = import_module("camera_" + os.environ["CAMERA"]).Camera
else:
    print("videostream")
    from camera_streamer import Camera

# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def index():
    """Video streaming home page."""
    if request.method == "POST":
        delay = int(request.data)
        print(delay)
        print(type(delay))
        return render_template("index.html", delay=delay)
    else:
        delay = 0
    return render_template("index.html", delay=delay)


def gen(camera):
    """Video streaming generator function."""
    yield b"--frame\r\n"
    while True:
        frame = camera.get_frame()
        yield b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n--frame\r\n"


@app.route("/video_feed/<delay>", methods=["POST", "GET"])
def video_feed(delay):
    """Video streaming route. Put this in the src attribute of an img tag."""
    print(f"video feed init with {delay}")
    cam = Camera(delay)
    return Response(gen(cam), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/delay_change", methods=["POST"])
def delay_change():
    print(request.data)
    return "yo"


if __name__ == "__main__":
    app.run(host="0.0.0.0", threaded=True, debug=True)
