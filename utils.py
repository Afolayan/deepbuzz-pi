import time
from datetime import datetime
from settings import *
from PIL import Image


def get_actual_image(filename):
    return Image.open(filename)


def get_time_in_millis():
    return int(round(time.time() * 1000))


def split_time_stings(date_string, delimiter):
    return date_string.split(delimiter)


def current_time_string():
    now = datetime.now()
    return now.strftime(get_date_format())


def get_date_format():
    time_delimiter = ":"
    day_delimiter = "-"

    now = datetime.now()
    hour = "%H"
    minute = "%M"
    second = "%S"
    day = "%D"
    month = "%M"
    year = "%Y"

    date_format = "".join([day, day_delimiter, month, day_delimiter,
                           year, " ", hour, time_delimiter, minute, time_delimiter, second])
    return date_format


def get_image_capture_time():
    return image_capture_time if image_capture_time else 30


def get_image_upload_time():
    return image_upload_time if image_upload_time else 30


def get_server_url():
    return server_url if server_url else "https://deepbuzz-project.azurewebsites.net/"


def get_server_url_with_hub():
    return "{0}{1}".format(server_url, device_hub_path)


def get_server_url_upload():
    return "{0}{1}".format(get_server_url(), "api/ImageUpload")
