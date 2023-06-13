from pyubx2 import UBXReader
import serial
import time


def start():
    serial_out = serial.Serial('/dev/ttyACM0', 9600, timeout=3)
    ubr = UBXReader(serial_out)
    try :
        (raw_data, parsed_data) = ubr.read()
        print(parsed_data)
        try:
            latitude = parsed_data.lat
            longitude = parsed_data.lon
            if latitude is None or longitude is None:
                return None
        except AttributeError:
            return None
        return {'latitude': latitude, 'longitude': longitude}
    except serial.serialutil.SerialException:
        print("Error reading from gps.")
        return None
