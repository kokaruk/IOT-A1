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
* This Module returns the reading of sensor data for usage in the program.
* There are two Parameters by default asString is 'y' for getting the reading as String with Unit
* or 'n' for only as float
* Further more sensorType reads by default t for temperature - calculated to account for the heat from the CPU
*    rt = regular temperature (without any calculations)
*    p = pressure
*    h = humidity
*    pt = temperature from pressure chip
*    ht = temperature from humidity chip
*    c = CPU Temperature
*
* Copyright notice - All copyrights belong to Dzmitry Kakaruk, Patrick Jacob - August 2018
"""

from sense_hat import SenseHat
import os

# instanciate senseHat Interface
sense = SenseHat()


# reading general temperature
def getReading(tostring='y', sensortype='t'):
    '''

    '''
    # reading 'regular' temperature - returning as string with unit
    if tostring == 'n' and sensortype == 'rt':
        temp = round(sense.get_temperature(), 2)
        return temp

    # reading 'regular' temperature - returning as string with unit
    elif tostring == 'y' and sensortype == 'rt':
        return str(getReading('n', 'rt')) + "°C"

    # reading pressure from pressure chip - returning as number (for DB)
    elif tostring == 'n' and sensortype == 'p':
        pressure = round(sense.get_pressure(), 2)
        return pressure

    # reading pressure from pressure chip - returning as string with unit
    elif tostring == 'y' and sensortype == 'p':
        return str(getReading('n', 'p')) + "mbar"

    # reading humidity from humidity chip - returning as number (for DB)
    elif tostring == 'n' and sensortype == 'h':
        humid = round(sense.get_humidity(), 2)
        return humid

    # reading humidity from humidity chip - returning as string with unit
    elif tostring == 'y' and sensortype == 'h':
        return str(getReading('n', 'h')) + "%"

    # calculating corrected Temperature from humidity chip - returning as number (for DB)
    # inspired by http://yaab-arduino.blogspot.com/2016/08/accurate-temperature-reading-sensehat.html
    elif tostring == 'n' and sensortype == 't':
        inter_temp = (getReading('n', 'ht') + getReading('n', 'pt')) / 2
        t_cpu = getReading('n', 'c')
        t_corr = round(inter_temp - ((t_cpu - inter_temp) / 1.5), 2)
        return t_corr

    # calculating corrected Temperature - returning as string with unit
    elif tostring == 'y' and sensortype == 't':
        return str(getReading('n', 't')) + "°C"

    # reading temperature from pressure chip - returning as number (for DB)
    elif tostring == 'n' and sensortype == 'pt':
        temp_p = round(sense.get_temperature_from_pressure(), 2)
        return temp_p

    # reading temperature from pressure chip - returning as string with unit
    if tostring == 'y' and sensortype == 'pt':
        return str(getReading('n', 'pt')) + "°C"

    # reading temperature from humidity chip  - returning as number (for DB)
    elif tostring == 'n' and sensortype == 'ht':
        temp_h = round(sense.get_temperature_from_humidity(), 2)
        return temp_h

    # reading temperature from humidity chip - returning as string with unit
    if tostring == 'y' and sensortype == 'ht':
        return str(getReading('n', 'ht')) + "°C"

    # reading cpu temperature from raspberry pi - returning as string with unit
    elif tostring == 'n' and sensortype == 'c':
        res = os.popen("vcgencmd measure_temp").readline()
        cpu_t = float(res.replace("temp=", "").replace("'C\n", ""))
        return cpu_t
    else:
        print('invalid operation')
