FROM python:3.11
RUN pip install --upgrade pip
RUN pip install bluepy RPIO requests
CMD ["python"]