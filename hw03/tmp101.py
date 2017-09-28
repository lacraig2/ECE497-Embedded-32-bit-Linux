#!/usr/bin/env python3
# Read a TMP101 sensor

import smbus
from time import sleep
import Adafruit_BBIO.GPIO as GPIO


bus = smbus.SMBus(1)
address = 0x48
address2 = 0x4A
bus.write_byte_data(address,1,0x6)
bus.write_byte_data(address,2,22)
bus.write_byte_data(address,3,27)
bus.write_byte_data(address2,1,0x6)
bus.write_byte_data(address2,2,22)
bus.write_byte_data(address2,3,27)
GPIO.setup("GP0_3", GPIO.IN)
GPIO.setup("GP0_4", GPIO.IN)

def print_temp(channel):
	print("ALERT")
	bus.write_byte_data(address,1,0x6)
	bus.write_byte_data(address2,1,0x6)
	# temp = bus.read_byte_data(address, 0)
	# temp2 = bus.read_byte_data(address2, 0)
	# print(str(temp)+ " "+str(temp2))

GPIO.add_event_detect("GP0_3", GPIO.BOTH, callback=print_temp)
GPIO.add_event_detect("GP0_4", GPIO.BOTH, callback=print_temp)
while True:
	temp = bus.read_byte_data(address, 0)
	temp2 = bus.read_byte_data(address2, 0)
	print(str(temp)+ " "+str(temp2))
	print(str(hex(bus.read_byte_data(address,1)))+" "+str(hex(bus.read_byte_data(address2,1))))
	sleep(0.5)
GPIO.cleanup()