#!/usr/bin/env python3
"""
* Authors : Patrick Jacob, Dzmitry Kakaruk,
*
* Version info 1.0.
*
* This program is created for Assignment 1 of Programming Internet of Things -  Course Master of IT - RMIT University.
* This code has parts which are inspired by the course material of  - Programming Internet of Things  - RMIT University.
*
* The purpose of the Program is to read the senseHat Data (Temperature, Humidity and Pressure)
* of a RaspberryPi and send to a Database and PushBullet.
* For more information please see: https://github.com/kokaruk/IOT-A1.
*
* This class searches for bluetooth devices nearby and displaying on the Pi the temperature, time and a welcome message
* Heavyly influenced by RMIT Programming Internet of Things  Semester 2 2018 Tutorial Week 5 - findmyphone.py
*
* Copyright notice - All copyrights belong to Dzmitry Kakaruk, Patrick Jacob - August 2018
"""
import os

import bluetooth
import json
import logging
import time
from sense_hat import SenseHat
import home_weather_station as ws
dir_path = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(dir_path, 'logs/weather_system_errors.log')
logging.basicConfig(filename=log_path,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%d-%m %H:%M:%S',
                    level=logging.INFO)


class BluetoothConnect:
    FILE_NAME = os.path.join(dir_path, 'conf/bluetooth_devices.json')

    # Main function
    def parse_known_devices(self):
        try:
            with open(self.FILE_NAME, "r") as known_device_file:
                return json.loads(known_device_file)
        except (FileNotFoundError, IOError):
            logging.critical(f"{self.FILE_NAME} not found")

    # Search for device based on device's name
    def search_and_display_message(self, **kwargs):
        devices = self.parse_known_devices()

        for devices["devices"].items in devices:
            name = devices["devices"]["name"]
            device = devices["devices"]["name"]
            while True:
                device_address = None
                dt = time.strftime("%a, %d %b %y %H:%M:%S", time.localtime())
                print("\nCurrently: {}".format(dt))
                time.sleep(3)  # Sleep three seconds
                nearby_devices = bluetooth.discover_devices()

                for mac_address in nearby_devices:
                    if device == bluetooth.lookup_name(mac_address, timeout=5):
                        device_address = mac_address
                        break
                if device_address is not None:
                    print("Hi {}! Your phone ({}) has the MAC address: {}".format(name, device, device_address))
                    temperature = ws.SenseHatReadings.get_reading_as_string(value=kwargs['temperature'],
                                                                            unit='temperature')

                    sense = SenseHat()
                    sense.show_message(f"Hi {name} Current Temp is {temperature}", scroll_speed=0.03)
                else:
                    print("Could not find target device nearby...")
