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

logging.basicConfig(filename="./logs/system_errors.log",
                    format='%(asctime)s %(message)s',
                    level=logging.CRITICAL)


# some code is used from https://simply-python.com/tag/pushbullet/

class PushMessage:
    FILE_NAME = './conf/API_KEY.txt'

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

    def push_message(self, title, body):
        """
        # Send a message to all your registered devices.
        :param title: title of the pushed message
        :param body: body body of the message
        """
        data = {
            'type': 'note',
            'title': title,
            'body': body
        }
        api_key = self.read_api_key()
        try:
            # sending of the message to push-bullet
            requests.post('https://api.pushbullet.com/api/pushes', data=data, auth=(api_key, ''))
        except requests.exceptions.RequestException as err:
            logging.critical(f" error pushing message {err}")
