from pyubx2 import UBXReader
import serial
import time


def start():
    serial_out = serial.Serial('/dev/ttyACM1', 9600, timeout=3)
    ubr = UBXReader(serial_out)
    (raw_data, parsed_data) = ubr.read()
    print(parsed_data)
    try :
        latitude = parsed_data.lat
        longitude = parsed_data.lon
    except AttributeError:
        return None
    return {'latitude': latitude, 'longitude': longitude}