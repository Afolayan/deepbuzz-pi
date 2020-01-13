# settings.py
import os

from flask.cli import load_dotenv

load_dotenv()

image_capture_time = os.getenv("IMAGE_CAPTURE_TIME")
image_upload_time = os.getenv("IMAGE_UPLOAD_TIME")
server_url = os.getenv("SERVER_URL")
data_upload_url = os.getenv("DATA_UPLOAD_URL")
device_hub_path = os.getenv("DEVICE_HUB_POST_FIX")
image_file_format = os.getenv("IMAGE_FILE_FORMAT")
maps_api_key = os.getenv("MAPS_API_KEY")
google_maps_base_url = os.getenv("GOOGLE_MAPS_BASE_URL")
device_name = "RaspBerryPi"
