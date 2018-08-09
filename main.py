import requests
import senseHatRead as s
from datetime import datetime

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

# insert into db
stmt = insert(data).values(dateTime = time,
                           temperature = s.getReading('n', 't'),
                           humidity = s.getReading('n', 'h'),
                           pressure = s.getReading('n', 'p'),)

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


# calling pushMessage function and sending Time, Temperature, Pressure and Humidity:
pushMessage(f"Current reading at {time}",
            f"Temperature: {s.getReading('y', 't')}{nl}"
            f"Pressure: {s.getReading('y', 'p')}{nl}"
            f"Humidity: {s.getReading('n', 't')}")
