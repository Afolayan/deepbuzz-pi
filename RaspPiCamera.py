import requests
from picamera import PiCamera
from utils import *
from time import sleep


def upload(filename, isImage=True):
    url = get_server_url_upload()
    print("url ==> {0}".format(url))

    path_img = os.getcwd() + "/%s" % filename
    with open(path_img, "rb") as dataFile:
        fullPathImage = os.path.basename(path_img)
        datum = {'FileName': filename, 'DateCreated': get_current_time()}
        if isImage:
            files = {'ImageFile': (fullPathImage, dataFile, 'multipart/form-data', {'Expires': '0'})}
        else:
            files = {'VideoFile': (fullPathImage, dataFile, 'multipart/form-data', {'Expires': '0'})}

        with requests.Session() as s:
            r = s.post(url, files=files, data=datum)

            print("content ==> {0}".format(r.content))
            print("json ==> {0}".format(r.json))

            return r.status_code


def get_current_time():
    now = datetime.now()
    return now


class DeepBuzzException(object):
    Exception

    def message(self):
        pass


class CameraOptions(object):
    isImage = False
    isVideo = False
    camera = None
    capture_time = get_image_capture_time()

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
                sleep(float(self.capture_time))  # wait some seconds
        except DeepBuzzException:
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
                    self.camera.close()
                    break

    def stop_capture(self):
        try:
            self.camera.stop_preview()
            self.camera.close()
            return "Camera closed successfully."
        except DeepBuzzException as exception:
            return "Cannot close camera: {0}".format(exception)