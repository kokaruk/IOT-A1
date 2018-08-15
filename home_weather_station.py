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
* This is the main class and serves as starting point of the program.
*
* Copyright notice - All copyrights belong to Dzmitry Kakaruk, Patrick Jacob - August 2018
"""

import configparser
import logging
import os
import sys
import time
from dataclasses import dataclass
from datetime import datetime

import influx_db_proxy as db
import push_message as pm
import sense_hat_read as sh


# import bluetooth as bt


@dataclass
class SenseHatReadings:
    temperature: float
    humidity: float
    pressure: float

    @staticmethod
    def get_reading_as_string(**kwargs) -> str:
        units_strings = {
            'temperature': '˚C',
            'humidity': '%',
            'pressure': 'mbar'
        }
        return f"{round(kwargs['value'], 2)}{units_strings[kwargs['unit']]}"


# Globals
dir_path = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(dir_path, 'logs/weather_system_errors.log')

logging.basicConfig(filename=log_path,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%d-%m %H:%M:%S',
                    level=logging.INFO)
# trying both json and ini for config reading
config = configparser.ConfigParser()
config_path = os.path.join(dir_path, 'conf/config.ini')
config.read(config_path)

try:
    temperature_threshold = int(config['Globals']['temperature_threshold'])
except KeyError:
    logging.critical("can't read config file")
    sys.exit(1)
last_temp: int
current_temperature = 0
current_time: str
RUNS_PER_MINUTE = 20
FREQUENCY = 3
sense_hat_readings: SenseHatReadings


def main():
    logging.info("Start Main")  # logging start for cron job monitoring
    for i in range(RUNS_PER_MINUTE):
        global current_time
        current_time = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        populate_readings()
        populate_db()
        send_notification()
        # check_for_bluetooth_devices()
        time.sleep(FREQUENCY)


def populate_readings():
    """
    # saving the senseHat Readings to a Dict
    """
    global sense_hat_readings
    sense_hat_readings = SenseHatReadings(temperature=sh.get_correct_temperature(),
                                          pressure=sh.get_sense_pressure(),
                                          humidity=sh.get_sense_humid())


def populate_db():
    # instantiating the database accessor
    database_accessor = db.InfluxDBProxy()

    # read last temperature entry from db
    global last_temp
    last_temp = database_accessor.get_last_logged()

    global current_temperature
    current_temperature = sense_hat_readings.temperature
    database_accessor.write_sh_readings(sense_hat_readings)


def send_notification():
    # todo fix here to evaluate average 15 minutes

    if not (last_temp or current_temperature <= temperature_threshold) or not (
            last_temp or current_temperature > temperature_threshold):
        # sending the pushMessage to PushBullet
        message = pm.PushMessage()
        message.push_message(time=current_time,
                             temperature=sense_hat_readings.temperature,
                             humidity=sense_hat_readings.humidity,
                             pressure=sense_hat_readings.pressure)


# def check_for_bluetooth_devices():
#   bluetooth_instance = bt.BluetoothConnect
#   bluetooth_instance.search_and_display_message(sense_hat_readings.temperature)


# calling main and starting the program
if __name__ == '__main__':
    main()
