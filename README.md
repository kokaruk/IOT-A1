# Assignment 1 Specification
_Assignment 1. IOT_
 
[You must stick to the standard style guide for your Python code](https://www.python.org/dev/peps/pep-0008/)
 
### Aim
 
The aim of this assignment is to write mini IoT applications using Raspberry Pi and Sense HAT in
Python language.
Some of the tasks of this assignment would require self-exploration and research, you will not find
the answer in lectures notes and/or tutorials.
 
### Tasks
Coding Tasks (20 marks)
 
 
- (10 marks) Testing the humidity every few milliseconds is fun, but not all that useful. Your
task is to build a data logger to record the humidity over time to a file, so we know how
damp (or not) the air in a lab/room/space is over the course of a week. To complete this task
  - set up a database (you can choose the type of database) with relevant columns for
humidity, temperature (anything else relevant that you can think of ) of the Raspberry Pi
 
Write Python code to
  - set up cron job to pull data from sense-hat at specific time interval,
  - put into database and
  - represent the data over a period using a web interface.
 
 
The more detailed and robust your data logger is, the more marks you will get. You need to
calibrate the temperature to account for warmer Raspberry Pi over time, dealing with
historical data (to avoid overwriting), etc.
 
- (5 marks) Write some Python code to have your Raspberry Pi push notifications to your
phone using Pushbullet when the room around your Raspberry Pi gets too cool (you can
assume anything less than 20 degrees C is cool) and reminds you to bring a sweater. The
fun part will be to integrate with the Pushbullet API.
iii. (5 marks) Write Python code to use Bluetooth on your Raspberry Pi to detect nearby devices
and greet the person whose device is registered with the Raspberry Pi and display the
current temperature. It is entirely up to you, how you will choose to represent the results.
But once again, anaemic representation will receive lower marks.
Code Elegance (10 marks)
 
- (4 marks) General code elegance, clarity and standard
 
- (6 marks) Professional use of version control system and how the code has been developed
over time. Low marks for code written over smaller time intervals.

---------
https://trello.com/b/k88JmZXD/assignment-1-piot Trelloboard of the project
