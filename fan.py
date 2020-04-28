# -*- coding: utf-* -*-

import os
from time import sleep
import time
import signal
import sys
import RPi.GPIO as GPIO
import smbus 
from threading import Thread 
bus = smbus.SMBus(1)

def get_fanspeed(tempval, configlist):
    for curconfig in configlist:
        curpair = curconfig.split("=")
        tempcfg = float(curpair[0])
        fancfg = int(float(curpair[1]))
        if tempval >= tempcfg:
            return fancfg
    return 0

def temp_check():
    fanconfig = ["65=100","60=75","55=50","45=25","40=10","39=0"]
    address = 0x1a
    prevblock = 0
    while True:
        temp = getCPUtemperature()
        val =float(temp)
        block = get_fanspeed(val, fanconfig)
        if block < prevblock:
            time.sleep(30)
        prevblock = block
        try:
            bus.write_byte(address, block)
        except IOError:
            temp= ""

        time.sleep(30)


def getCPUtemperature():
    res = os.popen('cat /sys/class/thermal/thermal_zone0/temp').readline()
    resn = float(res)
    temp = resn/1000
    #print("temp is {0}".format(temp)) #Uncomment here for testing
    return temp
	

#def attempt():
#    address = 0x1a
#    prevblock= 0 
#    block= [10,50,100,75,10,100,10]
#
#    for f in block:
#        
#        try:
#            bus.write_byte(address, f)
#            time.sleep(2)
#        except:
#            print("it broke ", sys.exc_info()[0])
#    
#    return block 

try:
    t1 = Thread(target=temp_check)
    t1.start()
except:
    t1.stop()
    GPIO.cleanup()
