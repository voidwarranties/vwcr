#!/usr/bin/env python
# coding=UTF8
<<<<<<< HEAD
# v 0.2
=======
# v 0.3
>>>>>>> added the wrong file first now the good one

import serial
import datetime

#global vars

<<<<<<< HEAD
def __init__():

  ser = serial.Serial("com11",9600)
=======
ser = serial.Serial("com11",9600) # windows
#ser = serial.Serial("/dev/ttyACM0" ,9600)# linux
>>>>>>> added the wrong file first now the good one

def price(getal1,getal2,getal3,getal4): # use this to print numbers directly (0-9 only) everything else will give a blank
  ser.write("P")
  ser.write(getal1)
  ser.write(getal2)
  ser.write(getal3)
  ser.write(getal4)
  ser.write("\n")

def time (hour,minu,sec): #use this to set the clock directly

  ser.write("T")
  ser.write(hour/10)
  ser.write(hour%10)
  ser.write(minu/10)
  ser.write(minu%10)
  ser.write(sec/10)
  ser.write(sec%10)
  ser.write("\n")

def state(): # get the drawerstate should be fine but might give randomness. The reseult should be either 1 or 0, aka a boolean. Might include a for loop to filter randomness.

  ser.write("S")
  state = ser.read()
  return(state)

def opendraw(): #open the drawer

  ser.write("O")

def settime():# set the time based on the system time

  now = datetime.datetime.now()
  ser.write("T")
  ser.write(int(now.hour)/10)
  ser.write(int(now.hour)%10)
  ser.write(int(now.minute)/10)
  ser.write(int(now.minute)%10)
  ser.write(int(now.second)/10)
  ser.write(int(now.second)%10)
  ser.write("\n")

  
