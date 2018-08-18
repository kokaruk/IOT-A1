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
import json
import logging
import os
from json import JSONDecodeError

import bluetooth

from config_constants import BLUETOOTH_DEVICES_JSON
from sense_hat_read import sense


def parse_known_devices() -> dict:
    try:
        with open(BLUETOOTH_DEVICES_JSON, "r") as known_device_file:
            return json.loads(known_device_file)
    except (FileNotFoundError, IOError, JSONDecodeError):
        logging.critical(f"{BLUETOOTH_DEVICES_JSON} failed to read")

    # Search for device based on device's name


def search_and_display_message(self, temperature):
    if os.path.exists(BLUETOOTH_DEVICES_JSON):
        known_devices = parse_known_devices()
        for known_devices["devices"].items in known_devices:
            owner_name = known_devices["devices"]["owner_name"]
            device_name = known_devices["devices"]["device_name"]
            while True:
                device_address = None

                nearby_devices = bluetooth.discover_devices()

                for mac_address in nearby_devices:
                    if device_name == bluetooth.lookup_name(mac_address, timeout=5):
                        device_address = mac_address
                        break
                if device_address is not None:
                    sense.show_message(f"Hi {owner_name} Current Temp is {temperature}", scroll_speed=0.03)
                else:
                    print("Could not find target device nearby...")
