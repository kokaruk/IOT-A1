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

from datetime import datetime
import sense_hat_read as s
import influx_db_proxy as db
import push_message as pm

time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
temperature_threshold = 25  # send notification when passing this temp threshold

def main():
    # saving the senseHat Readings to a Dict
    sense_hat_readings = {"temp": s.get_reading('n', 't'),
                          "pressure": s.get_reading('n', 'p'),
                          "humidity": s.get_reading('n', 'h')}

    # instantiating the database accessor
    database = db.InfluxDBProxy()

    # read last entry from db
    last_temp = database.get_last_logged()

    database.write_sh_readings(sense_hat_readings["temp"],
                               sense_hat_readings["pressure"],
                               sense_hat_readings["humidity"])

    #
    #  TODO: check if temperature change notification required
    #

    # TODO refactor: message construction should me in message module, not in main

    # sending the pushMessage to PushBullet
    title = 'It is warm enough for a t-shirt' \
        if s.get_reading('n', 't') >= temperature_threshold \
        else 'Please put on a Pullover - its getting colder'

    body = f"Current reading at {time} \n" \
           f"Temperature: {s.get_reading('y', 't')} \n" \
           f"Pressure: {s.get_reading('y', 'p')} \n" \
           f"Humidity: {s.get_reading('y', 'h')}"

    message = pm.PushMessage()
    message.push_message(title, body)


# calling main and starting the program
if __name__ == '__main__':
    main()
