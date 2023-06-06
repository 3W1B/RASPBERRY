import argparse
import time
import atexit

import lights
import gps

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

    lights.switch_status_light()

    inside_sensor = InsideSensor(args.serial_no)
    outside_sensor = OutsideSensor()

    api_service = ApiService(args.api_host, args.api_port)

    atexit.register(lights.cleanup)
    atexit.register(inside_sensor.disconnect)

    while True:

        outside_log = outside_sensor.start()
        inside_log = inside_sensor.start()

        # if lta radon is 0 - 75, green light
        # if lta radon is 75 - 100, yellow light
        # if lta radon is 100+, red light

        # if sta radon is 0 -4 , green light
        # if sta radon is 4 - 6, yellow light
        # if sta radon is 6+, red light

        lta_radon = inside_log["radon_lta"]
        sta_radon = inside_log["radon_sta"]

        if lta_radon <= 75:
            lta_light = "green"
        elif lta_radon <= 100:
            lta_light = "yellow"
        else:
            lta_light = "red"

        if sta_radon <= 4:
            sta_light = "green"
        elif sta_radon <= 6:
            sta_light = "yellow"
        else:
            sta_light = "red"

        if lta_light == "red" or sta_light == "red":
            lights.switch_red_light()
        elif lta_light == "yellow" or sta_light == "yellow":
            lights.switch_yellow_light()
        else:
            lights.switch_green_light()

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
                "radonLta": inside_log["radon_lta"],
                "radonSta": inside_log["radon_sta"],
            }
        }
        print(f"sending data to {args.api_host}:{args.api_port}/log/create -> {body}")
        response = api_service.post(body, "/log/create")
        print(f"response to {args.api_host}:{args.api_port}/log/create -> {response}")

        location = gps.start()
        while location is None:
            print("Retrying GPS location...")
            time.sleep(5)
            location = gps.start()
        body = {
            "loggerId": args.logger_id,
            "loggerPassword": args.logger_password,
            "latitude": location["latitude"],
            "longitude": location["longitude"],
        }
        print(f"sending data to {args.api_host}:{args.api_port}/location/update -> {body}")
        response = api_service.post(body, "/location/update")
        print(f"response to {args.api_host}:{args.api_port}/location/update -> {response}")
        time.sleep(120)