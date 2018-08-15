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
import os

from influxdb import InfluxDBClient
from influxdb import exceptions

dir_path = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(dir_path, 'logs/weather_system_errors.log')
logging.basicConfig(filename=log_path,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%d-%m %H:%M:%S',
                    level=logging.INFO)


class InfluxDBProxy:
    CONF_FILE = os.path.join(dir_path, 'conf/influx_connect.json')

    def __init__(self):
        connect = self.read_config_json()
        self._username = connect["user"]
        self._password = connect["password"]
        self._database = connect["database"]
        self._client = InfluxDBClient(host='localhost',
                                      port=8086,
                                      username=self._username,
                                      password=self._password,
                                      database=self._database)

    def read_config_json(self):
        try:
            with open(self.CONF_FILE, "r") as connect_file:
                return json.load(connect_file)
        except (FileNotFoundError, IOError):
            logging.critical(f"{self.CONF_FILE} not found")

    def write_sh_readings(self, temperature, humidity, pressure):
        """
        following this tutorial as basis: https://www.circuits.dk/datalogger-example-using-sense-hat-influxdb-grafana/
        heavily modified
        writing readings
        """

        try:
            # write measurements of DB
            write_data = [
                {
                    "measurement": "SenseHatReadings",
                    "tags": {"user": self._username},
                    "time": datetime.datetime.utcnow().isoformat(),
                    "fields": {
                        "temperature": temperature,
                        "humidity": humidity,
                        "pressure": pressure
                    }
                }
            ]

            result = self._client.write_points(write_data)

            # log if unsuccessful even
            if not result:
                logging.error(f"SenseHat to influxDatabase write : {result}")
        except exceptions.InfluxDBClientError as err:
            logging.critical(f"Error writing to the database{err}")

    def get_last_logged(self):
        """
        :return: read latest logged temperature data in db
        """
        try:
            # todo sql of last mean

            # SELECT mean("temperature")
            # FROM "SenseHatReadings"
            # WHERE ("user" = 'pi')
            # AND $timeFilter
            # GROUP BY time(15m) fill(0)

            # last_temp = self._client.query('SELECT LAST("temperature") FROM SenseHatReadings')
            # untested solution :
            # last_temp = self._client.query('SELECT MEAN(temperature) FROM SenseHatReadings where time >= (last(time) - 15m) and time <= now()')
            last_temp = self._client.query('SELECT LAST(mean("temperature")) FROM "SenseHatReadings" GROUP BY time(15m)')
            last_temp = list(last_temp.get_points())[0]
            return last_temp["last"]
        except exceptions.InfluxDBClientError as err:
            logging.critical(f"Error reading from the database{err}")
            return 0
