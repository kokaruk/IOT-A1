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

import os
import time
import json
from datetime import datetime, timedelta
from json import JSONDecodeError

from config import SenseHatReadings, UPPER_TEMPERATURE_THRESHOLD, LOWER_TEMPERATURE_THRESHOLD, \
    RUNS_PER_MINUTE, SLEEP_TIME, MESSENGER_FLAG_PATH, MESSAGE_HOLD, DATE_FORMAT, logger

from influx_db_proxy import InfluxDBProxy
from push_message import PushMessage
import sense_hat_read as sh
from bluetooth_mdl import search_and_display_message

messenger: PushMessage  # holds instance of push bullet messenger
database_accessor: InfluxDBProxy  # holds instance of database
sense_hat_readings: SenseHatReadings


def main():
    logger.info("start execution")
    global messenger
    global database_accessor
    messenger = PushMessage()  # init messenger
    database_accessor = InfluxDBProxy()  # init database accessor
    for i in range(RUNS_PER_MINUTE):
        populate_readings()
        write_readings_to_db()
        time.sleep(SLEEP_TIME)
    send_notification()
    search_and_display_message(temperature=database_accessor.get_last_average())


def populate_readings() -> None:
    """
    # saving the senseHat Readings to a global variable dict
    """
    global sense_hat_readings
    sense_hat_readings = SenseHatReadings(temperature=sh.get_correct_temperature(),
                                          pressure=sh.get_sense_pressure(),
                                          humidity=sh.get_sense_humid())


def write_readings_to_db() -> None:
    database_accessor.write_sh_readings(sense_hat_readings)


def send_notification() -> None:
    """
    Messaging method. Compare previous flag with current and sends push bullet message
    :return: None
    """

    flags = {}
    current_flag: str
    try:
        if os.path.exists(MESSENGER_FLAG_PATH):
            with open(MESSENGER_FLAG_PATH, "r") as flags_file:
                flags = json.load(flags_file)
    except JSONDecodeError:
        logger.error(f"error parsing JSON {MESSENGER_FLAG_PATH}")
    finally:
        if not flags:
            flags = {'flag': '',
                     'time': ''}

    try:
        average_temp = database_accessor.get_last_average()
        # set current flag
        if LOWER_TEMPERATURE_THRESHOLD <= average_temp <= UPPER_TEMPERATURE_THRESHOLD:
            current_flag = 'n'
        elif average_temp < LOWER_TEMPERATURE_THRESHOLD:
            current_flag = 'l'
        elif average_temp > UPPER_TEMPERATURE_THRESHOLD:
            current_flag = 'u'

        if current_flag is not 'n':
            current_time = datetime.now()
            current_time_str = current_time.strftime(DATE_FORMAT)
            if not flags['flag'] or \
                    current_flag is not flags['flag'] or \
                    hold_time_expired(flags, current_time):
                messenger.push_message(sense_hat_readings, time=current_time_str)
                logger.info("Sending Message")
                flags = {'flag': current_flag,
                         'time': current_time_str}
    except IndexError as err:  # if no data, don't push message (raised by database reader)
        logger.error(f"Empty DataSet, most likely no data in the last 15 min {err}")
    else:
        with open(MESSENGER_FLAG_PATH, "w") as flags_write:
            json.dump(flags, flags_write)


def hold_time_expired(flags: dict, current_time: datetime) -> bool:
    """
    Method to compute if messaging holding interval has expired, to avoid spamming
    :param flags: dict of messaging status
    :param current_time current system time
    :return: bool value
    """
    msg_time = datetime.strptime(flags['time'], DATE_FORMAT)
    hold_expiry = msg_time + timedelta(hours=MESSAGE_HOLD)
    return current_time >= hold_expiry


# calling main and starting the program
if __name__ == '__main__':
    main()
