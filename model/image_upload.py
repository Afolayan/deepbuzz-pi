# image_upload.py
from utils import *


class ImageUpload:
    def __init__(self, FileName):
        self.FileName = FileName
        self.DateCreated = get_time_in_millis()

    def set_filename(self, FileName):
        self.FileName = FileName
    
    def toString(self):
        return 'object has %s: %s' % (self.FileName, self.DateCreated)


class LocationUpload:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        self.date_created = get_time_in_millis()

    def set_location(self, location):
        self.latitude = location.latitude
        self.longitude = location.longitude
