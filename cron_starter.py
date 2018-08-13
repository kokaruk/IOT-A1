#!/usr/bin/env python3
#  * * * * * /home/pi/developer/python/iot/saytime.py
from crontab import CronTab

# init cron
cron = CronTab(user='pi')
cron.remove_all()

# add new cron job
job = cron.new(command='/home/pi/a1/home_weather_station.py')

# job settings
job.minute.every(1)
cron.write()
