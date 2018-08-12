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
* This Class is responsible for the passing of SenseHat Data to the Database
*
* Copyright notice - All copyrights belong to Dzmitry Kakaruk, Patrick Jacob - August 2018
"""

import datetime
import json
import logging

from influxdb import InfluxDBClient
from influxdb import exceptions

logging.basicConfig(filename="./logs/system_events.log", level=logging.INFO)
logging.basicConfig(filename="./logs/system_errors.log", level=logging.ERROR)


class DataBase:

    CONF_FILE = './conf/influx_connect.json'

    def __init__(self, temperature, humidity, pressure):
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure

    # following this tutorial as basis: https://www.circuits.dk/datalogger-example-using-sense-hat-influxdb-grafana/
    def influx(self):
        # json parsing from:  https://stackoverflow.com/questions/2835559/parsing-values-from-a-json-file
        try:
            with open(self.CONF_FILE, "r") as connect_file:
                connect = json.load(connect_file)

                # Assigning json attributes for connect to DB to variables
                host = connect["host"]
                port = connect["ip"]
                user = connect["user"]
                password = connect["password"]
                db = connect["database"]

                # calling the influx client
                client = InfluxDBClient(host, port, user, password, db)

                # write measures of Sensehat to DB
                write_data = [
                    {
                        "measurement": "SenseHatReadings",
                        "tags": {"user": user},
                        "time": datetime.datetime.utcnow().isoformat(),
                        "fields": {
                            "temperature": self.temperature,
                            "humidity": self.humidity,
                            "pressure": self.pressure
                        }
                    }
                ]

                result = client.write_points(write_data)

                # print result of writing to DB
                logging.info(f"SenserHat to influxDatabase: {result}")
        except exceptions.InfluxDBClientError as err:
            logging.error(err)
