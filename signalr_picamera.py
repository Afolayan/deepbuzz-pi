import json
import logging
import sys
import threading
from signalrcore.hub_connection_builder import HubConnectionBuilder
import requests as req

import requests
from flask import session
from PIL import Image
from utils import *
from time import sleep
import os
import socket

flask_url = "http://127.0.0.1:5000/"


def upload(filename, isImage=True):
    print("upload")
    file_path = os.getcwd() + "/%s" % filename
    # datum = {'FileName': filename, 'DateCreated': get_current_time(), 'IpAddress': session["ip_address"]}
    datum = {'FileName': filename, 'DateCreated': get_current_time(), 'IpAddress': "192.156.76.8"}

    if isImage:
        with open(file_path, "rb") as dataFile:
            fullPathImage = os.path.basename(file_path)
            files = {'ImageFile': (fullPathImage, dataFile, 'multipart/form-data', {'Expires': '0'})}
            url = get_image_upload_url()

            with requests.Session() as s:
                r = s.post(url, files=files, data=datum)

                return r.status_code
    else:
        print("MP4Box -add {0} {1}".format(filename, "video.mp4"))
        os.system("MP4Box -add {0} video.mp4".format(filename))

        output_video = os.getcwd() + "/video.mp4"

        with open(output_video, "rb") as dataFile:

            fullPathVideo = os.path.basename(output_video)
            files = {'VideoFile': (fullPathVideo, dataFile, 'multipart/form-data', {'Expires': '0'})}
            url = get_video_upload_url()
            with requests.Session() as s:
                r = s.post(url, files=files, data=datum)

                # remove the existing video file and recreate a new one
                os.system("rm video.mp4")
                os.system("touch video.mp4")

                return r.status_code


def get_current_time():
    now = datetime.now()
    return now


def try_and_verify_image(stream):
    image = Image.open(stream)
    print('Image is %dx%d' % image.size)
    image.verify()
    print('Image is verified')


class CameraOptions(threading.Thread):
    isImage = False
    isVideo = False
    camera = None
    capture_time = 0.3
    timestamp = datetime.now().strftime('%d-%m-%y_%H-%M-%S')

    def __init__(self, isVideo=False):
        self.killed = False
        if isVideo:
            threading.Thread.__init__(self, target=self.multiple_video_capture, args=(5,), name="upload_video")
        else:
            threading.Thread.__init__(
                self,
                target=self.multiple_image_capture,
                name="upload_image")
        self.daemon = True

    def start(self):
        self.__run_backup = self.run
        self.run = self.__run
        threading.Thread.start(self)

    def __run(self):
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame, event, arg):
        if event == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, event, arg):
        if self.killed:
            if event == 'line':
                raise SystemExit()
        return self.localtrace

    def kill(self):
        self.killed = True

    def multiple_image_capture(self):
        print("multiple_image_capture")
        self.init_camera()
        self.camera.start_preview()
        while True:
            try:
                for filename in self.camera.capture_continuous('img-65.jpg'):
                    print('Captured %s' % filename)

                    upload_status = upload(filename)
                    print("upload status code: {0}".format(upload_status))

                    if upload_status != 200:
                        self.stop_capture()
                        break
            except KeyboardInterrupt:
                self.stop_capture()
                sys.exit(0)

    def multiple_video_capture(self, count):
        print("multiple_video_capture")
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

    def stop_capture(self):
        try:
            self.camera.stop_preview()
            self.camera.close()
            self.thread.join()
            return "Camera closed successfully."
        except Exception as exception:
            return "Cannot close camera: {0}".format(exception)

    def init_camera(self):
        if not self.camera:
            from picamera import PiCamera
            self.camera = PiCamera()
            self.camera.resolution = (640, 480)


def onReceivedMessage(message):
    commandObject = message[0]
    commandItem = commandObject["item"]
    command = commandObject["command"]

    if commandItem == 'camera':
        cameraOptions = CameraOptions()
        if command == 'start':
            print("starting camera")
            cameraOptions.start()
        else:
            # for thread in threading.enumerate():
                # print("running threads: ", thread.name)
                # if thread.name == "upload_image":

            print("stopping camera")
            cameraOptions.kill()
            cameraOptions.join()
            if not cameraOptions.isAlive():
                print('thread killed')
            else:
                print('thread alive')

    elif commandItem == 'video':
        cameraOptions = CameraOptions(isVideo=True)
        if command == 'start':
            print("starting video")
            cameraOptions.thread.start()
        else:
            cameraOptions.terminate()
            cameraOptions.stop_capture()
    print("done command: " + commandItem)


def input_with_default(input_text, default_value):
    value = input(input_text.format(default_value))
    return default_value if value is None or value.strip() == "" else value


class SignalRCommands:
    server_url = "wss://deepbuzz-project.azurewebsites.net/commandHub"

    username = "jeff"

    def __init__(self):
        super().__init__()
        self.hub_connection = HubConnectionBuilder() \
            .with_url(self.server_url) \
            .configure_logging(logging.DEBUG) \
            .with_automatic_reconnect({
            "type": "raw",
            "keep_alive_interval": 10,
            "reconnect_interval": 5,
            "max_attempts": 5
        }).build()

    def run(self):
        self.setup_connection(onReceivedMessage)

    def setup_connection(self, onReceivedCommand):
        print("SignalRCommands: setup_connection")

        self.hub_connection.on_open(lambda: print("connection opened and handshake received ready to send messages"))
        self.hub_connection.on_close(lambda: print("connection closed"))

        self.hub_connection.on("SendCommand", onReceivedCommand)
        self.hub_connection.start()
        message = None

        while message != "exit()":
            message = input(">> ")
            if message is not None and message is not "" and message is not "exit()":
                self.hub_connection.send("SendMessage", [self.username, message])

    def close_connection(self):
        self.hub_connection.stop()
        sys.exit(0)


SERVER_ADDRESS = (HOST, PORT) = '', 3500
REQUEST_QUEUE_SIZE = 5


if __name__ == '__main__':
    commandsHub = SignalRCommands()
    commandsHub.run()
