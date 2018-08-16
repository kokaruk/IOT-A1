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
* For more information please see: https://github.com/kokaruk/IOT-A1
* This Class is responsible for the passing of the Pushbullet Message
*
* Copyright notice - All copyrights belong to Dzmitry Kakaruk, Patrick Jacob - August 2018
"""

import logging
import requests

from config_constants import UPPER_TEMPERATURE_THRESHOLD, API_KEY_FILE, SenseHatReadings


# some code is used from https://simply-python.com/tag/pushbullet/

class PushMessage:

    def __init__(self):
        self._api_key = PushMessage.read_api_key()

    @staticmethod
    def read_api_key() -> str:
        """
        read out of the local API Key
        :return: push-bullet api key
        """
        try:
            with open(API_KEY_FILE, "r") as api_key:
                return api_key.read()
        except (FileNotFoundError, IOError):
            logging.critical(f"{API_KEY_FILE} not found")

    def push_message(self, sense_hat_readings: SenseHatReadings, time: str) -> None:
        """
        # Send a message to all your registered devices.
        :param sense_hat_readings data from sense hat
        :param time current time
        """

        title = 'It is warm enough for a t-shirt' \
            if sense_hat_readings.temperature >= UPPER_TEMPERATURE_THRESHOLD \
            else 'Please put on a Pullover - its getting colder'

        temperature = sense_hat_readings.get_reading_as_string(value=sense_hat_readings.temperature, unit='temperature')
        pressure = sense_hat_readings.get_reading_as_string(value=sense_hat_readings.pressure, unit='pressure')
        humidity = sense_hat_readings.get_reading_as_string(value=sense_hat_readings.humidity, unit='humidity')

        body = f"Current reading at {time}\n" \
               f"Temperature: {temperature}\n" \
               f"Pressure: {pressure}\n" \
               f"Humidity: {humidity}"

        data = {
            'type': 'note',
            'title': title,
            'body': body
        }

        try:
            # sending off the message to push-bullet
            requests.post('https://api.pushbullet.com/api/pushes',
                          data=data, auth=(self._api_key, ''))
        except requests.exceptions.RequestException as err:
            logging.critical(f" error pushing message {err}")
