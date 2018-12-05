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
import os
import time
import multiprocessing
from json import JSONDecodeError

import bluetooth

from config import BLUETOOTH_DEVICES_JSON, BLUETOOTH_STATUS_JSON, BLUETOOTH_GREETING_DELAY, logger
from sense_hat_read import sense


def parse_known_devices() -> dict:
    """
    parsing known bluetooth devices list
    """
    with open(BLUETOOTH_DEVICES_JSON, "r") as known_device_file:
            return json.load(known_device_file)


def search_and_display_message(temperature: float) -> None:
    if os.path.exists(BLUETOOTH_DEVICES_JSON):
        try:
            known_devices = parse_known_devices()
            for device in known_devices["devices"]:
                is_home = bluetooth.lookup_name(device['mac'], timeout=15)
                if os.path.exists(BLUETOOTH_STATUS_JSON):
                    with open(BLUETOOTH_STATUS_JSON) as bluetooth_status_file:
                        bt_stat = json.load(bluetooth_status_file)
                else:
                    bt_stat = {'sent': False}
                if is_home is not None and not bool(bt_stat['sent']):    # if device is home and greeting wasn't sent
                    # make a process on separate thread
                    multiprocessing.Process(target=sensehat_greeting, args=(temperature, device,)).start()
                    bt_stat['sent'] = True
                elif is_home is None:
                    bt_stat['sent'] = False
                with open(BLUETOOTH_STATUS_JSON, "w") as status_write:
                    json.dump(bt_stat, status_write)
        except (FileNotFoundError, IOError, JSONDecodeError):
            logger.critical(f"{BLUETOOTH_DEVICES_JSON} failed to read")


def sensehat_greeting(temperature: float, device: dict) -> None:
    """
    process to send greetings on sense hat from se[arate sthread
    """
    logger.log("Bluetooth greetings")

    time.sleep(BLUETOOTH_GREETING_DELAY)

    sense.show_message(f"Hi {device['owner_name']} Current Temp is {round(temperature,2)} C",
                       scroll_speed=0.1, text_colour=(65, 96, 68), back_colour=(255, 149, 139))
    sense.clear()
