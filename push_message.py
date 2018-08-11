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

import requests


# some code is used from https://simply-python.com/tag/pushbullet/

class PushMessage:
    FILE_NAME = './API_KEY.txt'

    def __init__(self, title, body):
        self.title = title
        self.body = body

    # Send a message to all your registered devices.
    def push_message(self):
        data = {
            'type': 'note',
            'title': self.title,
            'body': self.body
        }
        # read out of the local API Key
        file = open(self.FILE_NAME, mode='r')  # 'r' is to read
        api_key = file.read()
        file.close()

        # sending of the message to pushbullet
        requests.post('https://api.pushbullet.com/api/pushes', data=data, auth=(api_key, ''))
