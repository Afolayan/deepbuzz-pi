# image_upload.py
from utils import *


class ImageUpload:
    def __init__(self, image_file, filename):
        self.image_file = image_file
        self.filename = filename
        self.date_created = get_time_in_millis()

    def set_filename(self, filename):
        self.filename = filename

    def set_image_file(self, image_file):
        self.image_filee = image_file


class LocationUpload:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        self.date_created = get_time_in_millis()

    def set_location(self, location):
        self.latitude = location.latitude
        self.longitude = location.longitude
