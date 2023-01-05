#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response, request, url_for, redirect

# import camera driver
if os.environ.get("CAMERA"):
    Camera = import_module("camera_" + os.environ["CAMERA"]).Camera
else:
    from camera_opencv import Camera

# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

app = Flask(__name__)


@app.route("/", defaults={"text": "default"})
@app.route("/<text>")
def index(text):
    """Video streaming home page."""
    return render_template("index.html",text=text)


@app.route("/", methods=["POST"])
def index_post():
    text = request.form["text"]
    processed_text = text.upper()
    return redirect(url_for("index",text=text))


def gen(camera):
    """Video streaming generator function."""
    yield b"--frame\r\n"
    while True:
        frame = camera.get_frame()
        yield b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n--frame\r\n"


@app.route("/video_feed/<text>")
def video_feed(text):
    """Video streaming route. Put this in the src attribute of an img tag."""
    print(f"video feed init {text}")
    cam = Camera()
    return Response(gen(cam), mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    app.run(host="0.0.0.0", threaded=True)
