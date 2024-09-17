from flask import Flask, render_template, Response
from picamera2 import Picamera2, Preview
from libcamera import controls
import cv2
import numpy as np

# Initialize Flask app
app = Flask(__name__)

# Initialize Picamera2
camera = Picamera2()
# rotate images automatically by 90 degrees
camera.set_rotation(90)

# Create a configuration for video streaming (you can adjust this as needed)
camera_config = camera.create_video_configuration()
camera.configure(camera_config)

# Start the camera
camera.start()

def generate_frames():
    while True:
        # Capture frame-by-frame from the Picamera2
        frame = camera.capture_array()

        # Convert the frame to a JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Yield the frame in a format suitable for Flask video streaming
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(generate_frames(),


