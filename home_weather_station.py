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

import logging
import time
from datetime import datetime
from config_constants import SenseHatReadings, UPPER_TEMPERATURE_THRESHOLD, LOWER_TEMPERATURE_THRESHOLD, \
    RUNS_PER_MINUTE, FREQUENCY, MESSENGER_FLAG_PATH

from influx_db_proxy import InfluxDBProxy
from push_message import PushMessage
import sense_hat_read as sh

# import bluetooth as bt


messenger: PushMessage  # holds instance of push bullet messenger
database_accessor: InfluxDBProxy  # holds instance of database
sense_hat_readings: SenseHatReadings


def main():
    logging.info("Start Main")  # logging start for cron job monitoring
    global messenger
    global database_accessor
    messenger = PushMessage()  # init messenger
    database_accessor = InfluxDBProxy()  # init database accessor
    for i in range(RUNS_PER_MINUTE):
        populate_readings()
        write_readings_to_db()
        # check_for_bluetooth_devices()
        time.sleep(FREQUENCY)
    send_notification()


def populate_readings():
    """
    # saving the senseHat Readings to a global variable dict
    """
    global sense_hat_readings
    sense_hat_readings = SenseHatReadings(temperature=sh.get_correct_temperature(),
                                          pressure=sh.get_sense_pressure(),
                                          humidity=sh.get_sense_humid())


def write_readings_to_db():
    global current_temperature
    current_temperature = sense_hat_readings.temperature
    database_accessor.write_sh_readings(sense_hat_readings)


def send_notification() -> None:
    """
    Messaging method. Compare previous flag with current and sends push bullet message
    :return: None
    """
    current_time = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    current_flag: str
    try:
        with open(MESSENGER_FLAG_PATH, "r") as flags:
            last_flag = flags.read()
            if last_flag is '':
                last_flag = 'n'
    except (FileNotFoundError, IOError):
        logging.error(f"{MESSENGER_FLAG_PATH} not found")
        last_flag = 'n'  # assuming normal temperature if failing to read flag file

    try:
        average_temp: int = database_accessor.get_last_average()
        # set current flag
        if LOWER_TEMPERATURE_THRESHOLD <= average_temp <= UPPER_TEMPERATURE_THRESHOLD:
            current_flag = 'n'
        elif average_temp < LOWER_TEMPERATURE_THRESHOLD:
            current_flag = 'l'
        elif average_temp > UPPER_TEMPERATURE_THRESHOLD:
            current_flag = 'u'
        # compare flags
        if current_flag is not 'n' and current_flag is not last_flag:
            messenger.push_message(sense_hat_readings, time=current_time)
            logging.info("Sending Message")
        # write flag
    except IndexError as err:  # if no data, don't push message
        logging.error(f"Empty DataSet, most likely no data in the last 15 min {err}")
    with open(MESSENGER_FLAG_PATH, "w") as flags:
        flags.write(current_flag)


# def check_for_bluetooth_devices():
#   bluetooth_instance = bt.BluetoothConnect
#   bluetooth_instance.search_and_display_message(sense_hat_readings.temperature)


# calling main and starting the program
if __name__ == '__main__':
    main()
