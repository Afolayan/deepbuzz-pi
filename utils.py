import time
from datetime import datetime
import os
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
    return image_capture_time


def get_server_url():
    return server_url


def get_server_url_with_hub():
    return "{0}{1}".format(server_url, device_hub_path)
