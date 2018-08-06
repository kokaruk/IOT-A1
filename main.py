from sense_hat import SenseHat
from datetime import datetime
import requests
import os
import json

# Import Table, Column, String, Integer, Float, Boolean from sqlalchemy
from sqlalchemy import Table, Column, String, Integer, Float, insert, create_engine, MetaData

# https://www.pythonsheets.com/notes/python-sqlalchemy.html#insert-create-an-insert-statement
# creation of sqldb and engine
engine = create_engine('sqlite:///iot.sqlite')
meta = MetaData(engine)

# Define a new table with dateTime, temperature, humidity, and pressure and place columns: data
data = Table('data', meta,
             Column('dateTime', String(255), unique=True),  # DateTime
             Column('temperature', Float()),
             Column('humidity', Float()),
             Column('pressure', Float()),
             Column('place', String(255))  # location yet to be set
             )

# Use the metadata to create the table
meta.create_all(engine)

# set time
time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# instanciate senseHat Interface
sense = SenseHat()

# using low lights for the sense hat display
sense.low_light = True

# reading general temperature
temp = str(round(sense.get_temperature())) + "°C"
print("General Temperature Reading: " + temp)

# reading pressure from pressure reader
pressure = str(round(sense.get_pressure())) + "mbar"
print("Pressure reading: " + pressure)

# reading temperature from pressure reader
temp_p = round(sense.get_temperature_from_pressure())
print("Temperature from pressure chip: " + temp_p)

# reading humidity reader
humid = str(round(sense.get_humidity())) + "%"
print("Humidity reading: " + humid)

# reading temperature from humidity reader
temp_h = round(sense.get_temperature_from_humidity())
print("Temperature from humidity chip: " + temp_h)


# inspired by http://yaab-arduino.blogspot.com/2016/08/accurate-temperature-reading-sensehat.html

def get_cpu_temp():
    res = os.popen("vcgencmd measure_temp").readline()
    t = float(res.replace("temp=", "").replace("'C\n", ""))
    return t


def temp():
    inter_temp = (temp_h + temp_p)
    t_cpu = get_cpu_temp()
    t_corr = inter_temp - ((t_cpu - inter_temp) / 1.5)
    return t_corr


print(temp())

# insert into db
stmt = insert(data).values(dateTime=time, temperature=round(temp()),
                           humidity=round(sense.get_humidity()), pressure=round(sense.get_pressure()))

# connect to db and append insert
connection = engine.connect()
results = connection.execute(stmt)

filename = '/home/pi/Desktop/API_KEY.txt'
file = open(filename, mode='r')  # 'r' is to read
API_KEY = file.read()
file.close()


# Send a message to all your registered devices.
def pushMessage(title, body):
    data = {
        'type': 'note',
        'title': title,
        'body': body
    }
    resp = requests.post('https://api.pushbullet.com/api/pushes', data=data, auth=(API_KEY, ''))


# variable for new line for the push message
nl = "\n"

# calling pushMessage function and sending Time, Temperature, Pressue and Humidity:
pushMessage("Current reading at " + time,
            "Temperature: " + temp + nl + "Pressure: " + pressure + nl + "Humidity: " + humid)
