import io
import json
import socket
import struct

import requests
from flask import session
from PIL import Image
from utils import *
from time import sleep
import os


def upload(filename, isImage=True):
    print("upload")
    file_path = os.getcwd() + "/%s" % filename
    datum = {'FileName': filename, 'DateCreated': get_current_time(), 'IpAddress': session["ip_address"]}

    if isImage:
        with open(file_path, "rb") as dataFile:
            fullPathImage = os.path.basename(file_path)
            files = {'ImageFile': (fullPathImage, dataFile, 'multipart/form-data', {'Expires': '0'})}
            url = get_image_upload_url()

            with requests.Session() as s:
                r = s.post(url, files=files, data=datum)

                print("content ==> {0}".format(r.content))
                print("json ==> {0}".format(r.json))

                return r.status_code
    else:
        # use this one file for all videos, so we wont clutter the pi
        print("MP4Box -add {0} {1}".format(filename, "video.mp4"))
        os.system("MP4Box -add {0} video.mp4".format(filename))

        # print("MP4Box -add {} {}".format("my_video.h264", "video.mp4"))
        # os.system("MP4Box -add my_video.h264 video.mp4")

        output_video = os.getcwd() + "/video.mp4"
        print("output_video is " + output_video)

        with open(output_video, "rb") as dataFile:

            fullPathVideo = os.path.basename(output_video)
            files = {'VideoFile': (fullPathVideo, dataFile, 'multipart/form-data', {'Expires': '0'})}
            print("files is {}".format(files))
            url = get_video_upload_url()

            print("url ==> {0}".format(url))
            with requests.Session() as s:
                r = s.post(url, files=files, data=datum)

                print("content ==> {0}".format(r.content))
                print("json ==> {0}".format(r.json))

                # remove the existing video file and recreate a new one
                os.system("rm video.mp4")
                os.system("touch video.mp4")

                return r.status_code


def get_current_time():
    now = datetime.now()
    return now


def tryAndVerifyImage(stream):
    image = Image.open(stream)
    print('Image is %dx%d' % image.size)
    image.verify()
    print('Image is verified')


class CameraOptions(object):
    isImage = False
    isVideo = False
    camera = None
    # capture_time = get_image_capture_time()
    capture_time = 0.3
    timestamp = datetime.now().strftime('%d-%m-%y_%H-%M-%S')

    def __init__(self):
        # from picamera import PiCamera
        # self.camera = PiCamera()
        # self.camera.resolution = (640, 480)
        pass

    def single_image_capture(self):
        print("single_image_capture")
        self.init_camera()
        self.camera.start_preview()
        sleep(2)
        filename = "foo.jpg"
        self.camera.capture(filename)
        print('Captured %s' % filename)
        upload_status = upload(filename)
        print("upload status code: {0}".format(upload_status))
        sleep(float(get_image_capture_time()))  # wait some seconds

    def multiple_image_capture(self):
        print("multiple_image_capture")
        self.init_camera()
        self.camera.start_preview()
        sleep(2)
        try:
            # for filename in self.camera.capture_continuous('img-{timestamp:%Y-%m-%d-%H-%M-%S}.jpg'):
            for filename in self.camera.capture_continuous('img-65.jpg'):
                print('Captured %s' % filename)

                upload_status = upload(filename)
                print("upload status code: {0}".format(upload_status))

                if upload_status != 200:
                    self.stop_capture()
                    break
                sleep(self.capture_time)  # wait some seconds
        except Exception as e:
            self.stop_capture()
            return "Cannot complete this process."

    def single_video_capture(self):
        print("single_video_capture")
        self.init_camera()
        filename = 'my_video.h264'
        print(" started now at {}".format(self.timestamp))
        self.camera.start_preview()
        self.camera.start_recording(filename)
        sleep(30)
        self.camera.stop_recording()
        self.camera.stop_preview()
        print(" ended now at {}".format(self.timestamp))
        upload(filename, False)

    def multiple_video_capture(self, count):
        print("multiple_video_capture")
        if count == 1:
            print("\n\ni is single_video_capture")
            self.single_video_capture()
        else:
            self.init_camera()
            self.camera.start_preview()
            for filename in \
                    self.camera.record_sequence('%d.h264' % i for i in range(1, int(count))):
                self.camera.wait_recording(self.capture_time)

                upload_status = upload(filename, False)
                print("upload status code: {0}".format(upload_status))

                if upload_status != 200:
                    self.camera.stop_recording()
                    self.camera.close()
                    break
            #self.camera.stop_recording()

            # for i in range(1, int(count)):
            #     print("\n\ni is {0}".format(i))
            #     self.single_video_capture()
            #     sleep(5)

    def stop_capture(self):
        try:
            self.camera.stop_preview()
            self.camera.close()

            return "Camera closed successfully."
        except Exception as exception:
            return "Cannot close camera: {0}".format(exception)

    def init_camera(self):
        if not self.camera:
            from picamera import PiCamera
            self.camera = PiCamera()
            self.camera.resolution = (640, 480)
