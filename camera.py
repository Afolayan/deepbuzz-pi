from picamera import PiCamera
from time import sleep
from datetime import datetime
import time
from utils import *
import threading
import urllib
from image_upload import *
import requests


def capture_image():
    camera = PiCamera()
    ##camera.rotation = 180
    camera.start_preview()
    sleep(5)
    now = datetime.now()
    current_time = get_time_in_millis()+""

    image_capture_dir = '/home/pi/Documents/deepbuzz/images/'
    image_file_name = image_capture_dir.join([current_time, image_file_format])

    camera.capture(image_file_name)
    camera.stop_preview()

    return image_file_name


def create_upload_object(filename):
    image_upload = ImageUpload(
        image_file=get_actual_image(filename),
        filename=filename
    )


def upload(upload_object):
    url = "{0}{1}".format(server_url, data_upload_url)
    print("url ==> {0}".format(url))
    request = requests.post(url, data=upload_object)
    ##urllib.urlopen(url)
    return request.status_code


def continuous_capture():
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.start_preview()
    sleep(2)
    for filename in camera.capture_continuous('img{timestamp:%Y-%m-%d-%H-%M-%S}.jpg'):
        print('Captured %s' % filename)
        upload_object = create_upload_object(filename)
        upload(upload_object)
        sleep(image_capture_time)  # wait some seconds


def start():
    # capture and upload image here
    continuous_capture()
    print("HTTP request sent")


start()