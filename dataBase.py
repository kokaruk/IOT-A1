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

# Import Table, Column, String, Integer, Float, Boolean from sqlalchemy
from sqlalchemy import Table, Column, String, Integer, Float, insert, create_engine, MetaData
from datetime import datetime


class dataBase:

    def __init__(self, temperature, humidity, pressure):
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure

    # some code is used from https://www.pythonsheets.com/notes/python-sqlalchemy.html#insert-create-an-insert-statement
    # creation of sqlite DB and engine
    def insert(self):
        engine = create_engine('sqlite:///iot.sqlite')
        meta = MetaData(engine)

        # Define a new table with dateTime, temperature, humidity, and pressure and place columns: data
        data = Table('data', meta,
                     Column('dateTime', String(255), unique=True),  # DateTime
                     Column('temperature', Float()),
                     Column('humidity', Float()),
                     Column('pressure', Float())
                     )

        # Use the metadata to create the table
        meta.create_all(engine)

        # set time
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # insert into db
        stmt = insert(data).values(dateTime=time,
                                   temperature=self.temperature,
                                   humidity=self.humidity,
                                   pressure=self.pressure)

        # connect to db and append insert
        connection = engine.connect()
        connection.execute(stmt)
