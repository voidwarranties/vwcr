#!/usr/bin/env python
# coding=UTF8
# v 0.8


import serial
import datetime
import math

#global vars


ser = serial.Serial("com11",9600)# windows
#ser = serial.Serial("/dev/ttyACM0" ,9600)# linux


def price(getal): # use this to print numbers
  getal2 = str(format(getal, "05.2f")).replace(".","")
  ser.write("P" + getal2 + "\n")


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

  
