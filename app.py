import requests
from flask import Flask, render_template, Response, json, session
from datetime import datetime
from utils import get_device_registration_url, get_device_name
from RaspPiCamera import CameraOptions, get_current_time

app = Flask(__name__)
cameraOptions = CameraOptions()

# vc = cv2.VideoCapture(0)


@app.route('/')
def index():
    """Video streaming"""
    now = datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")

    register_url = get_device_registration_url()
    with requests.Session() as s:
        data = {'DeviceName': get_device_name(), 'DateCreated': get_current_time()}
        headers = {"Content-Type": "application/json"}
        r = s.post(register_url, headers=headers, data=data)

        json_response = json.dumps(r.json())
        print("json response == " + json_response)
        print("json response == "+json_response["data"].ipAddress)

    session['ip_address'] = json_response.data.ipAddress

    templateData = {
        'title': 'HELLO!',
        'time': timeString,
        'response': json_response,
        'ipaddress': json_response.data.ipAddress
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
    cameraOptions.multiple_image_capture()
    return json.dumps({'success': True, "function": "start"}), 200, {'ContentType': 'application/json'}


@app.route('/camera/stop', methods=['POST'])
def stop_camera():
    message = cameraOptions.stop_capture()
    message_ = {
        "success": True,
        "function": "stop",
        "message": message
    }
    return json.dumps(message_), 200, {'ContentType': 'application/json'}


@app.route('/video/start', methods=['POST'])
def start_video():
    # if request.json:
    #     count = request.json["count"]
    # else:
    #     count = 11
    #cameraOptions.multiple_video_capture(2)
    cameraOptions.single_video_capture()

    return json.dumps({'success': True, "function": "start"}), 200, {'ContentType': 'application/json'}


@app.route('/video/stop', methods=['POST'])
def stop_video():
    message = cameraOptions.stop_capture()
    message_ = {'success': True,
                "function": "stop",
                "message": message
                }
    return json.dumps(message_), 200, {'ContentType': 'application/json'}


@app.route('/location/start', methods=['POST'])
def start_location():
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/location/stop', methods=['POST'])
def stop_location():
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True, port=80)
