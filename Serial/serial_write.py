#!/usr/bin/env python

import time
import serial

ser = serial.Serial(
   port='/dev/ttyAMA0',
   baudrate = 9600,
   parity=serial.PARITY_NONE,
   stopbits=serial.STOPBITS_ONE,
   bytesize=serial.EIGHTBITS,
   timeout=1
)
counter=0


while (counter < 100):
   ser.write('Write counter: %d \n'%(counter))
   time.sleep(10)
   counter += 1