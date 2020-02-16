"""
    GPS Interfacing with Raspberry Pi using Python http://www.electronicwings.com
    """
import requests
import socket
import serial  # import serial pacakge
from time import sleep
import webbrowser  # import package for opening link in browser
import sys  # import system package

url = "https://deepbuzz-project.azurewebsites.net/api/Location"


def GPS_Info():
    global NMEA_buff
    global lat_in_degrees
    global long_in_degrees
    nmea_time = []
    nmea_latitude = []
    nmea_longitude = []
    print(NMEA_buff)
    nmea_time = NMEA_buff[0]  # extract time from GPGGA string
    nmea_latitude = NMEA_buff[1]  # extract latitude from GPGGA string
    nmea_longitude = NMEA_buff[3]  # extract longitude from GPGGA string

    print("NMEA Time: ", nmea_time, '\n')
    print("NMEA Latitude:", nmea_latitude, "NMEA Longitude:", nmea_longitude, '\n')

    if not nmea_latitude or not nmea_longitude:
        return
    lat = float(nmea_latitude)  # convert string into float for calculation
    longi = float(nmea_longitude)  # convert string into float for calculation

    lat_in_degrees = convert_to_degrees(lat)  # get latitude in degree decimal format
    long_in_degrees = convert_to_degrees(longi)  # get longitude in degree decimal format


# convert raw NMEA string into degree decimal format
def convert_to_degrees(raw_value):
    decimal_value = raw_value / 100.00
    degrees = int(decimal_value)
    mm_mmmm = (decimal_value - int(decimal_value)) / 0.6
    position = degrees + mm_mmmm
    position = "%.4f" % (position)
    return position


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


gpgga_info = "$GPGGA,"
ser = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1)  # Open port with baud rate
GPGGA_buffer = 0
NMEA_buff = 0
lat_in_degrees = 0
long_in_degrees = 0
try:
    while True:
        received_data = (str)(ser.readline())  # read NMEA string received
        GPGGA_data_available = received_data.find(gpgga_info)  # check for NMEA GPGGA string
        if GPGGA_data_available > 0:
            GPGGA_buffer = received_data.split("$GPGGA,", 1)[1]  # store data coming after "$GPGGA," string
            NMEA_buff = (GPGGA_buffer.split(','))  # store comma separated data in buffer
            GPS_Info()  # get time, latitude, longitude

            print("lat in degrees:", lat_in_degrees, " long in degree: ", long_in_degrees, '\n')
            datum = {'DeviceId': get_ip(), 'Longitude': long_in_degrees, 'Latitude': lat_in_degrees}

            with requests.Session() as s:
                r = s.post(url, data=datum)

                print("content ==> {0}".format(r.content))
                print("json ==> {0}".format(r.json))


except KeyboardInterrupt:
    sys.exit(0)
