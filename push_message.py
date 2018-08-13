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
import configparser
import logging

import requests

import sense_hat_read as sh

logging.basicConfig(filename="/home/pi/a1/weather_system_errors.log",
                    format='%(asctime)s %(message)s',
                    level=logging.CRITICAL)

config = configparser.ConfigParser()
config.read('/home/pi/a1/conf/config.ini')
# send notification when passing this temp threshold
temperature_threshold = int(config['Globals']['temperature_threshold'])


# some code is used from https://simply-python.com/tag/pushbullet/

class PushMessage:
    FILE_NAME = '/home/pi/a1/conf/API_KEY.txt'

    def read_api_key(self):
        """
        read out of the local API Key
        :return: push-bullet api key
        """
        try:
            with open(self.FILE_NAME, "r") as api_key:
                return api_key.read()
        except (FileNotFoundError, IOError):
            logging.critical(f"{self.FILE_NAME} not found")

    def push_message(self, **kwargs):
        """
        # Send a message to all your registered devices.
        :param kwargs dictionary
        """

        title = 'It is warm enough for a t-shirt' \
            if kwargs['temperature'] >= temperature_threshold \
            else 'Please put on a Pullover - its getting colder'

        temperature = sh.get_reading_as_string(value=kwargs['temperature'], unit='temperature')
        pressure = sh.get_reading_as_string(value=kwargs['pressure'], unit='pressure')
        humidity = sh.get_reading_as_string(value=kwargs['humidity'], unit='humidity')

        body = f"Current reading at {kwargs['time']}\n" \
               f"Temperature: {temperature}\n" \
               f"Pressure: {pressure}\n" \
               f"Humidity: {humidity}"

        data = {
            'type': 'note',
            'title': title,
            'body': body
        }
        api_key = self.read_api_key()
        try:
            # sending of the message to push-bullet
            requests.post('https://api.pushbullet.com/api/pushes',
                          data=data, auth=(api_key, ''))
        except requests.exceptions.RequestException as err:
            logging.critical(f" error pushing message {err}")
