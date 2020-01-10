from time import sleep

import requests
from picamera import PiCamera

from utils import *

camera = PiCamera()
camera.resolution = (640, 480)


def capture_image():
    ##camera.rotation = 180
    camera.start_preview()
    sleep(5)
    now = datetime.now()
    current_time = get_time_in_millis() + ""

    image_capture_dir = '/home/pi/Documents/deepbuzz/images/'
    image_file_name = image_capture_dir.join([current_time, image_file_format])

    camera.capture(image_file_name)
    camera.stop_preview()

    return image_file_name


def get_current_time():
    now = datetime.now()

    print("now =", now)

    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print("date and time =", dt_string)

    return now


def upload(filename):
    url = get_server_url_upload()
    print("url ==> {0}".format(url))

    headers = {'Content-Type': 'application/json'}

    path_img = os.getcwd() + "/%s" % filename
    with open(path_img, "rb") as image_file:
        name_img = os.path.basename(path_img)
        files = {'ImageFile': (name_img, image_file, 'multipart/form-data', {'Expires': '0'})}
        datum = {'FileName': filename, 'DateCreated': get_current_time()}
        with requests.Session() as s:
            r = s.post(url, files=files, data=datum)

            print("request body == {0}".format(r.request))
            print("request ==> {0}".format(r))
            print("content ==> {0}".format(r.content))
            print("json ==> {0}".format(r.json))
            print("headers ==> {0}".format(r.headers))
            print("raw is: {0} ".format(r.raw))
            print("raw is: {0} ".format(r.text))

            print(r.status_code)

            return r.status_code


def continuous_capture(status=0):
    camera.start_preview()
    sleep(2)
    if status == 0:
        for filename in camera.capture_continuous('img-{timestamp:%Y-%m-%d-%H-%M-%S}.jpg'):
            print('Captured %s' % filename)
            upload_status = upload(filename)
            print("upload status code: {0}".format(upload_status))
            if upload_status != 200:
                camera.close()
                break
            sleep(float(get_image_capture_time()))  # wait some seconds
    elif status == 1:
        camera.stop_preview()
        camera.close()


def start():
    # capture and upload image here
    continuous_capture()
    print("HTTP request sent")


def stop():
    # stop capturing and uploading image
    try:
        camera.stop_preview()
        camera.close()
        return "Camera stopped"
    except Exception:
        return "Cannot stop camera"
