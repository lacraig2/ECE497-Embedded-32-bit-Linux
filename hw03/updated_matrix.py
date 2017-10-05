#!/usr/bin/env python3
# Read a TMP101 sensor

import smbus
from time import sleep
import Adafruit_BBIO.GPIO as GPIO


bus = smbus.SMBus(1)
address = 0x48
address2 = 0x4A
bus.write_byte_data(address,1,0b0110000)
bus.write_i2c_block_data(address,2,[0b00010100,0b0000])
bus.write_i2c_block_data(address,3,[0b00011011,0b0000])
bus.write_byte_data(address2,1,0b0110000)
bus.write_i2c_block_data(address2,2,[0b00010100, 0b0000])
bus.write_i2c_block_data(address2,3,[0b00011011,0b0000])

def print_temp(channel):
	print(channel)
	#bus.write_byte_data(address,1,0x0)
	#bus.write_byte_data(address2,1,0x0)
	# temp = bus.read_byte_data(address, 0)
	# temp2 = bus.read_byte_data(address2, 0)
	# print(str(temp)+ " "+str(temp2))
GPIO.setup("GP0_3", GPIO.IN)
GPIO.setup("GP0_4", GPIO.IN)
GPIO.add_event_detect("GP0_3", GPIO.BOTH, callback=print_temp)
GPIO.add_event_detect("GP0_4", GPIO.BOTH, callback=print_temp)
while True:
	temp = bus.read_byte_data(address, 0)
	temp2 = bus.read_byte_data(address2, 0)
	print("temp from both ", str(temp)+ " "+str(temp2))
	#print("1 from both: ",str(bin(bus.read_word_data(address,1)))+" "+str(bin(bus.read_word_data(address2,1))))
	#print("2 and 3 from one " ,bin(bus.read_word_data(address,2)),bin(bus.read_word_data(address,3)))
	#print(bus.read_word_data(address,1))
	sleep(0.5)
GPIO.cleanup()
