#from sense_hat import SenseHat
from datetime import datetime
import requests

import sense_hat_read as s
import sys
#print sys.getdefaultencoding()

# Import Table, Column, String, Integer, Float, Boolean from sqlalchemy
from sqlalchemy import Table, Column, String, Integer, Float, insert, create_engine, MetaData

p_test = s.getReading('y', 'p') #pressure
t_test = s.getReading('y', 't') #calc temperature
h_test = s.getReading('y', 'h') #humidity

print(f"temp {t_test}, pressure: {p_test}, humidity: {h_test}")


# https://www.pythonsheets.com/notes/python-sqlalchemy.html#insert-create-an-insert-statement
# creation of sqldb and engine
#engine = create_engine('sqlite:///iot.sqlite')
#meta = MetaData(engine)

# Define a new table with dateTime, temperature, humidity, and pressure and place columns: data
#data = Table('data', meta,
#             Column('dateTime', String(255), unique=True),  # DateTime
#             Column('temperature', Float()),
#             Column('humidity', Float()),
#             Column('pressure', Float()),
#             Column('place', String(255))  # location yet to be set
#             )



# Use the metadata to create the table
#meta.create_all(engine)

# set time
time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


# insert into db
#stmt = insert(data).values(dateTime=time, temperature=round(sense.get_temperature()),
#                           humidity=round(sense.get_humidity()), pressure=round(sense.get_pressure()))

# connect to db and append insert
#connection = engine.connect()
#results = connection.execute()#stmt)

#filename = '/home/pi/Desktop/API_KEY.txt'
#file = open(filename, mode='r')  # 'r' is to read
#API_KEY = file.read()
#file.close()


# Send a message to all your registered devices.
#def pushMessage(title, body):
#    data = {
#        'type': 'note',
#        'title': title,
#        'body': body
#    }
#    resp = requests.post('https://api.pushbullet.com/api/pushes', data=data, auth=(API_KEY, ''))


# variable for new line for the push message
nl = "\n"


# calling pushMessage function and sending Time, Temperature, Pressue and Humidity:
#pushMessage("Current reading at " + time,
#            "Temperature: " + str(temp) + nl + "Pressure: " + pressure + nl + "Humidity: " + humid)
