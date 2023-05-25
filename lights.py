import RPi.GPIO as GPIO
import time
from enum import Enum

class RadonLight(Enum):
    RED = 20,
    GREEN = 21,
    BLUE = 16

class StatusLight(Enum):
    RED = 19,
    GREEN = 13,
    BLUE = 26

GPIO.setmode(GPIO.BCM)

GPIO.setup(RadonLight.RED.value, GPIO.OUT)
GPIO.setup(RadonLight.GREEN.value, GPIO.OUT)
GPIO.setup(RadonLight.BLUE.value, GPIO.OUT)
GPIO.setup(StatusLight.RED.value, GPIO.OUT)
GPIO.setup(StatusLight.GREEN.value, GPIO.OUT)
GPIO.setup(StatusLight.BLUE.value, GPIO.OUT)

def switch_status_light():
    GPIO.output(StatusLight.RED.value, False)
    GPIO.output(StatusLight.GREEN.value, False)
    GPIO.output(StatusLight.BLUE.value, True)

def switch_red_light():
    GPIO.output(RadonLight.RED.value, True)
    GPIO.output(RadonLight.GREEN.value, False)
    GPIO.output(RadonLight.BLUE.value, False)

def switch_green_light():
    GPIO.output(RadonLight.RED.value, False)
    GPIO.output(RadonLight.GREEN.value, True)
    GPIO.output(RadonLight.BLUE.value, False)

def switch_yellow_light():
    GPIO.output(RadonLight.RED.value, True)
    GPIO.output(RadonLight.GREEN.value, True)
    GPIO.output(RadonLight.BLUE.value, False)

def cleanup():
    GPIO.cleanup()