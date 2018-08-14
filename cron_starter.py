#!/usr/bin/env python3
import os

from crontab import CronTab


def reset() -> int:
    prompt = "reset all cron jobs? "
    while True:
        try:
            return {"true": True, "false": False}[input(prompt).lower()]
        except KeyError:
            print("Invalid input please enter True or False!")


# init cron
cron = CronTab(user='pi')
reset_cron: bool = reset()

if reset_cron:
    cron.remove_all()

# add new cron job
dir_path = os.path.dirname(os.path.abspath(__file__))
main_path = os.path.join(dir_path, 'home_weather_station.py')

job = cron.new(command=main_path)

# job settings
job.minute.every(1)
cron.write()
