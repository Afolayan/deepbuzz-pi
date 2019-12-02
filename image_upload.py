# image_upload.py
from utils import *


class ImageUpload:
    def __init__(self, ImageFile, FileName):
        self.ImageFile = ImageFile
        self.FileName = FileName
        self.date_created = get_time_in_millis()

    def set_filename(self, FileName):
        self.FileName = FileName

    def set_image_file(self, ImageFile):
        self.ImageFile = ImageFile


class LocationUpload:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        self.date_created = get_time_in_millis()

    def set_location(self, location):
        self.latitude = location.latitude
        self.longitude = location.longitude
