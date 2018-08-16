"""
* Authors : Patrick Jacob, Dzmitry Kakaruk
*
* Version info 1.0.
*
* This program is created for Assignment 1 of Programming Internet of Things -  Course Master of IT - RMIT University.
* This code has parts which are inspired by the course material of  - Programming Internet of Things  - RMIT University.
*
* The purpose of the Program is to read the senseHat Data (Temperature, Humidity and Pressure)
* of a RaspberryPi and send to a Database and PushBullet.
* For more information please see: https://github.com/kokaruk/IOT-A1
* This Module returns the reading of sensor data for usage in the program.
*
* Copyright notice - All copyrights belong to Dzmitry Kakaruk, Patrick Jacob - August 2018
"""

import os
from statistics import mean
from sense_hat import SenseHat

from config_constants import TEMP_FACTOR_COMP

sense = SenseHat()


def _get_sense_temperature_from_humidity() -> float:
    return sense.get_temperature_from_humidity()


def _get_sense_temperature_from_pressure() -> float:
    return sense.get_temperature_from_pressure()


def _get_sense_cpu_temperature() -> float:
    res = os.popen("vcgencmd measure_temp").readline()
    res = float(res.replace("temp=", "").replace("'C\n", ""))
    return res


def get_sense_pressure() -> float:
    return sense.get_pressure()


def get_sense_humid() -> float:
    return sense.get_humidity()


def get_correct_temperature() -> float:
    """
    # calculating corrected Temperature from humidity chip - returning as number
    # inspired by http://yaab-arduino.blogspot.com/2016/08/accurate-temperature-reading-sensehat.html
    :return: correct temp
    """
    inter_temp = mean((_get_sense_temperature_from_humidity(), _get_sense_temperature_from_pressure()))
    t_cpu = _get_sense_cpu_temperature()
    t_corr = inter_temp - ((t_cpu - inter_temp) / TEMP_FACTOR_COMP)
    return t_corr
