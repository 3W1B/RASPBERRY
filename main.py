import argparse
import time

from inside_sensor import InsideSensor
from outside_sensor import OutsideSensor
from api_service import ApiService

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="main.py", description="Airthings Wave sensor data logger")
    parser.add_argument("--serial_no", type=int, help="Airthings device serial number found under the magnetic backplate.")
    parser.add_argument("--api_host", type=str, help="API host address")
    parser.add_argument("--api_port", type=int, help="API port")
    parser.add_argument("--logger_id", type=str, help="Logger ID")
    parser.add_argument("--logger_password", type=str, help="Logger password")
    args = parser.parse_args()

    if args.serial_no is None:
        parser.error("The serial_no argument is required.")

    if args.api_host is None:
        parser.error("The api_host argument is required.")

    if args.api_port is None:
        parser.error("The api_port argument is required.")

    if args.logger_id is None:
        parser.error("The logger_id argument is required.")

    if args.logger_password is None:
        parser.error("The logger_password argument is required.")

    inside_sensor = InsideSensor(args.serial_no)
    outside_sensor = OutsideSensor()

    api_service = ApiService(args.api_host, args.api_port)

    while True:

        outside_log = outside_sensor.start()
        inside_log = inside_sensor.start()

        body = {
            "loggerId": args.logger_id,
            "loggerPassword": args.logger_password,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime()),
            "logOutside": {
                "temperature": outside_log["temperature"],
                "humidity": outside_log["humidity"],
            },
            "logInside": {
                "temperature": inside_log["temperature"],
                "humidity": inside_log["humidity"],
                "radon": inside_log["radon_sta"],
            }
        }

        api_service.post(body)
        time.sleep(150)