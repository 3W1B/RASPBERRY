from typing import Dict

import RPi.GPIO as GPIO
import time
from datetime import datetime
from datetime import timedelta
import board
import busio
import adafruit_am2320

i2c = busio.I2C(board.SCL, board.SDA)

class OutsideSensor:
    def __init__(self):
        self.sensor = adafruit_am2320.AM2320(i2c)

    def start(self):
        return {
            'humidity': format(self.sensor.relative_humidity),
            'temperature': format(self.sensor.temperature)
        }