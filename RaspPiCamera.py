import requests
from gevent.subprocess import call
from picamera import PiCamera
from utils import *
from time import sleep
import os


def upload(filename, isImage=True):

    path_img = os.getcwd() + "/%s" % filename
    with open(path_img, "rb") as dataFile:
        fullPathImage = os.path.basename(path_img)
        datum = {'FileName': filename, 'DateCreated': get_current_time()}
        if isImage:
            files = {'ImageFile': (fullPathImage, dataFile, 'multipart/form-data', {'Expires': '0'})}
            url = get_image_upload_url()
        else:
            # timestamp = datetime.now().strftime('%d-%m-%y_%H-%M-%S')

            # use this one file for all videos, so we wont clutter the pi
            output_video = "/home/pi/Documents/deepbuzz/deepbuzz-pi/video_file.mp4"
            # call(["MP4Box", "-add", dataFile, output_video])

            os.system("MP4Box -add {} {}".format(dataFile, output_video))
            files = {'VideoFile': (fullPathImage, output_video, 'multipart/form-data', {'Expires': '0'})}
            print(files)
            url = get_video_upload_url()

        print("url ==> {0}".format(url))
        with requests.Session() as s:
            r = s.post(url, files=files, data=datum)

            print("content ==> {0}".format(r.content))
            print("json ==> {0}".format(r.json))

            return r.status_code


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
    ## capture_time = get_image_capture_time()
    capture_time = 2

    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = (640, 480)

    def single_image_capture(self):
        self.camera.start_preview()
        sleep(2)
        filename = "foo.jpg"
        self.camera.capture(filename)
        print('Captured %s' % filename)
        upload_status = upload(filename)
        print("upload status code: {0}".format(upload_status))
        sleep(float(get_image_capture_time()))  # wait some seconds

    def multiple_image_capture(self):
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
        filename = 'my_video.h264'
        self.camera.start_recording(filename)
        self.camera.wait_recording(self.capture_time)
        self.camera.stop_recording()
        upload(filename, False)

    def multiple_video_capture(self, count):
        if count == 1:
            self.single_video_capture()
        else:
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
