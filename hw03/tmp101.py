#!/usr/bin/python

# By: Luke Craig
# Dr. Yoder
# ECE497 Embedded 32-bit Linux
# HW04


import smbus
from time import sleep
import Adafruit_BBIO.GPIO as GPIO


bus = smbus.SMBus(1) 					# set up the smbus

address = 0x48							# addresses for two i2c temp sensors
address2 = 0x4A

bus.write_byte_data(address,1,0x6)		# set up the configuration register for i2c temp sensor
bus.write_byte_data(address,2,22)		# set up T_low for i2c temp sensor
bus.write_byte_data(address,3,27)		# set up T_high for i2c temp sensor
bus.write_byte_data(address2,1,0x6)		# set up the configuration register for i2c temp sensor
bus.write_byte_data(address2,2,22)		# set up T_low for i2c temp sensor
bus.write_byte_data(address2,3,27)		# set up T_high for i2c temp sensor

GPIO.setup("GP0_3", GPIO.IN)			# set up pin to listen for ALERT pin
GPIO.setup("GP0_4", GPIO.IN)			# set up pin to listen for ALERT pin

def print_temp(channel):				# set up callback method
	print("ALERT")


#attach callbacks to two pins
GPIO.add_event_detect("GP0_3", GPIO.BOTH, callback=print_temp)
GPIO.add_event_detect("GP0_4", GPIO.BOTH, callback=print_temp)

# loop over and wait
while True:
	sleep(0.5)
GPIO.cleanup()							# no reason to be leaving a mess