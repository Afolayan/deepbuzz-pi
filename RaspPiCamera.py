import requests
from flask import session
from gevent.subprocess import call

from utils import *
from time import sleep
import os


def upload(filename, isImage=True):

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
        print("MP4Box -add {} {}".format("my_video.h264", "video.mp4"))
        os.system("MP4Box -add my_video.h264 video.mp4")
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

# path_img = os.getcwd() + "/%s" % filename
#     with open(path_img, "rb") as dataFile:
#         fullPathImage = os.path.basename(path_img)
#         datum = {'FileName': filename, 'DateCreated': get_current_time(), 'IpAddress': session["ip_address"]}
#         if isImage:
#             files = {'ImageFile': (fullPathImage, dataFile, 'multipart/form-data', {'Expires': '0'})}
#             url = get_image_upload_url()
#
#             with requests.Session() as s:
#                 r = s.post(url, files=files, data=datum)
#
#                 print("content ==> {0}".format(r.content))
#                 print("json ==> {0}".format(r.json))
#
#                 return r.status_code
#         else:
#             # timestamp = datetime.now().strftime('%d-%m-%y_%H-%M-%S')
#
#             # use this one file for all videos, so we wont clutter the pi
#             output_video = "/home/pi/video_file.mp4"
#             fullPathVideo = os.path.basename(output_video)
#             with open(output_video, 'r+') as outputVideo:
#                 print("MP4Box -add {} {}".format(dataFile, outputVideo))
#                 os.system("MP4Box -add my_video.h264 video.mp4")
#                 files = {'VideoFile': (output_video, outputVideo, 'multipart/form-data', {'Expires': '0'})}
#                 print("files is {}".format(files))
#                 url = get_video_upload_url()
#
#                 print("url ==> {0}".format(url))
#                 with requests.Session() as s:
#                     r = s.post(url, files=files, data=datum)
#
#                     print("content ==> {0}".format(r.content))
#                     print("json ==> {0}".format(r.json))
#
#                     return r.status_code


def get_current_time():
    now = datetime.now()
    return now


class DeepBuzzException(object):
    BaseException

    def message(self):
        pass


class CameraOptions(object):
    isImage = False
    isVideo = False
    camera = None
    # capture_time = get_image_capture_time()
    capture_time = 2
    timestamp = datetime.now().strftime('%d-%m-%y_%H-%M-%S')

    def __init__(self):
        # from picamera import PiCamera
        # self.camera = PiCamera()
        # self.camera.resolution = (640, 480)
        pass

    def single_image_capture(self):
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
        self.init_camera()
        self.camera.start_preview()
        sleep(2)
        try:
            for filename in self.camera.capture_continuous('img-{timestamp:%Y-%m-%d-%H-%M-%S}.jpg'):
                print('Captured %s' % filename)

                upload_status = upload(filename)
                print("upload status code: {0}".format(upload_status))

                if upload_status != 200:
                    self.stop_capture()
                    break
                sleep(self.capture_time)  # wait some seconds
        except DeepBuzzException:
            self.stop_capture()
            return "Cannot complete this process."

    def single_video_capture(self):
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
        if count == 1:
            self.single_video_capture()
        else:
            self.init_camera()
            self.camera.start_preview()
            for filename in \
                    self.camera.record_sequence('%d.h264' % i for i in range(1, count)):
                self.camera.wait_recording(self.capture_time)

                upload_status = upload(filename, False)
                print("upload status code: {0}".format(upload_status))

                if upload_status != 200:
                    self.camera.stop_recording()
                    self.camera.close()
                    break
            self.camera.stop_recording()

    def stop_capture(self):
        try:
            self.camera.stop_preview()
            # self.camera.close()
            return "Camera closed successfully."
        except DeepBuzzException as exception:
            return "Cannot close camera: {0}".format(exception)

    def init_camera(self):
        if not self.camera:
            from picamera import PiCamera
            self.camera = PiCamera()
            self.camera.resolution = (640, 480)
