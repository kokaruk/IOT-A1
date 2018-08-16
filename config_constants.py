"""
* Authors : Patrick Jacob, Dzmitry Kakaruk
*
* Version info 1.0.
*
* This program is created for Assignment 1 of Programming Internet of Things -  Course Master of IT - RMIT University.
* This code has parts which are inspired by the course material of  - Programming Internet of Things  - RMIT University.
*
* The purpose of this module is a unified storage of all constant values
*
* Copyright notice - All copyrights belong to Dzmitry Kakaruk, Patrick Jacob - August 2018
"""
import configparser
import os
import logging
import sys
from dataclasses import dataclass


# all module constants

DIR_PATH = os.path.dirname(os.path.abspath(__file__))  # getting current file absolute path, required for cron jobs
LOG_PATH = os.path.join(DIR_PATH, 'logs/weather_system_errors.log')

# init logging
logging.basicConfig(filename=LOG_PATH,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%d-%m %H:%M:%S',
                    level=logging.INFO)

config = configparser.ConfigParser()  # reading config from ini file
config_path = os.path.join(DIR_PATH, 'conf/config.ini')
config.read(config_path)

# send notification when passing this temp threshold
try:
    LOWER_TEMPERATURE_THRESHOLD = int(config['Globals']['lower_temperature_threshold'])
    UPPER_TEMPERATURE_THRESHOLD = int(config['Globals']['upper_temperature_threshold'])
except KeyError:
    logging.critical("can't read config file")
    sys.exit(1)

# SENSE  HAT MODULE CONSTANTS
TEMP_FACTOR_COMP = 1.5  # this is a specified temp factor for compensating proximity of HAT sensor to CPU

# PUSH MESSAGE CONSTANTS
API_KEY_FILE = os.path.join(DIR_PATH, 'conf/API_KEY.txt')

# main module constants
try:
    RUNS_PER_MINUTE = int(config['Globals']['runs_per_minute'])
except KeyError:
    logging.critical("can't read config file")
    sys.exit(1)
FREQUENCY: int = int(60 / RUNS_PER_MINUTE)  # 60 seconds in a minute
MESSENGER_FLAG_PATH = os.path.join(DIR_PATH, 'conf/m_flags')


@dataclass
class SenseHatReadings:
    temperature: float
    humidity: float
    pressure: float

    @staticmethod
    def get_reading_as_string(value: float, unit: str) -> str:
        units_strings = {
            'temperature': '˚C',
            'humidity': '%',
            'pressure': 'mbar'
        }
        return f"{round(value, 2)}{units_strings[unit]}"
