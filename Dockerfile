FROM python:3.11
RUN pip install --upgrade pip
RUN pip install bluepy RPIO requests pyubx2 adafruit-circuitpython-am2320
CMD ["python"]
