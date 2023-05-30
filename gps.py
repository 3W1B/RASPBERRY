from pyubx2 import UBXReader
import serial
import time


def start():
    serial_out = serial.Serial('/dev/ttyACM0', 9600, timeout=3)
    ubr = UBXReader(serial_out)
    (raw_data, parsed_data) = ubr.read()
    try :
        latitude = parsed_data.lat
        longitude = parsed_data.lon
    except AttributeError:
        latitude = None
        longitude = None
    return {'latitude': latitude, 'longitude': longitude}