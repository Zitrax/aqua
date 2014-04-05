#!/usr/bin/python

import os
import glob
import time
 
os.system('/sbin/modprobe w1-gpio')
os.system('/sbin/modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
 
def read_temp_raw():
    with open(device_file, 'r') as f:
        return f.readlines()
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        print "CRC check failed, retrying"
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f
    

def sse():
    print "Content-Type: text/event-stream\n"
    print "Event: aqua-temp"
    for i in xrange(1):
        print "data: %s\n" % read_temp()[0]

sse()
