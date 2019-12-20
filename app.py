from flask import Flask, render_template, Response, json
from datetime import datetime
# import picamera
# import cv2
import socket
import io
import StartCamera

app = Flask(__name__)


# vc = cv2.VideoCapture(0)


@app.route('/')
def index():
    """Video streaming"""
    now = datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
        'title': 'HELLO!',
        'time': timeString
    }
    return render_template('index.html', **templateData)


def gen():
    """Video streaming generator function."""
    while True:
        yield "yeah"
        # rval, frame = vc.read()
        # cv2.imwrite('t.jpg', frame)
        # yield (b'--frame\r\n'
        #       b'Content-Type: image/jpeg\r\n\r\n' + open('t.jpg', 'rb').read() + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/camera/start', methods=['POST'])
def start_camera():
    StartCamera.start()
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/camera/stop', methods=['POST'])
def stop_camera():
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/location/start', methods=['POST'])
def start_location():
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/location/stop', methods=['POST'])
def stop_location():
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True, port=80)
