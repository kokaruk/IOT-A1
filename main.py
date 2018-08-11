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
import database as db
import pushMessage as pM

time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def main():
    # saving the senseHat Readings to a Dict
    sense_hat_readings = {"temp": s.getReading('n', 't'),
                          "pressure": s.getReading('n', 'p'),
                          "humidity": s.getReading('n', 'h')}

    # instantiating the database with the sense_hat data
    database = db.dataBase(sense_hat_readings["temp"], sense_hat_readings["pressure"], sense_hat_readings["humidity"])
    database.influx()

    # sending the pushMessage to PushBullet - need both a
    if s.getReading('n', 't') >= 18:

        title = 'It is warm enough for a t-shirt'
    else:
        title = 'Please put on a Pullover - its getting colder'

    body = f"Current reading at {time} \n" \
           f"Temperature: {s.getReading('y', 't')} \n" \
           f"Pressure: {s.getReading('y', 'p')} \n" \
           f"Humidity: {s.getReading('y', 'h')}"

    message = pM.pushMessage(title, body)
    message.pushMessage()


# calling main and starting the program
if __name__ == '__main__': main()
